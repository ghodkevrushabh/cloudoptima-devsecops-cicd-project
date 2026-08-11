pipeline {
    agent any

    parameters {
        string(
            name: 'APP_NAME',
            defaultValue: 'demo-payment-api-2',
            description: 'Application infrastructure directory name'
        )

        string(
            name: 'APP_REPO_URL',
            defaultValue: 'https://github.com/ghodkevrushabh/demo-payment-api.git',
            description: 'Application source repository'
        )
    }

    environment {
        TF_DIR = "terraform/${params.APP_NAME}"
        ANSIBLE_DIR = "ansible/${params.APP_NAME}"
    }

    stages {

        stage('Checkout Infrastructure Code') {
            steps {
                checkout scm
            }
        }

        stage('Checkout Application Source') {
            steps {
                dir('application') {
                    deleteDir()

                    git(
                        branch: 'main',
                        url: "${params.APP_REPO_URL}"
                    )
                }
            }
        }

        stage('Validate Application') {
            steps {
                sh '''
                    set -e

                    echo "=== Application files ==="
                    ls -la application/

                    echo "=== Python syntax check ==="
                    python3 -m py_compile application/app.py

                    echo "Application validation passed."
                '''
            }
       }
        
       stage('Debug SonarQube Tool') {
           steps {
               script {
                    def scannerHome = tool 'SonarQubeScanner'

                    sh """
                        echo "scannerHome=${scannerHome}"
                        echo "PATH=\$PATH"
                        ls -lah "${scannerHome}"
                        ls -lah "${scannerHome}/bin"
                        "${scannerHome}/bin/sonar-scanner" --version
                    """
                }
            }
       }     
       
       stage('SecOps: Code Quality - SonarQube') {
           steps {
               script {
                   def scannerHome = tool 'SonarQubeScanner'
                   
                   withCredentials([
                       string(
                           credentialsId: 'sonarqube-token',
                           variable: 'SONAR_TOKEN'
                       )
                   ]) {
                      sh '''
                          set -e
                          echo "=== SonarQube Code Analysis ==="

                          "${scannerHome}/bin/sonar-scanner" \
                            -Dsonar.projectKey=cloudoptima \
                            -Dsonar.projectName=CloudOptima \
                            -Dsonar.sources=application \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.token="\$SONAR_TOKEN"
                      '''
                   }
               }
           }
       }

       stage('SecOps: Secret Scan - GitLeaks') {
           steps {
               sh '''
                   set -e

                   echo "=== GitLeaks Secret Scan ==="

                   gitleaks detect \
                   --source . \
                   --no-banner

                   echo "GitLeaks scan passed."
               '''
            }
        }

        stage('SecOps: IaC Scan - Checkov') {
            steps {
                sh '''
                    set -e
                    checkov -d "${TF_DIR}" --soft-fail
                '''
            }
        }

        stage('SecOps: IaC Scan - Trivy') {
            steps {
                sh '''
                    set -e
                    trivy config "${TF_DIR}"
                '''
            }
        }

        stage('FinOps: Infracost') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'infracost-api-key',
                        variable: 'INFRACOST_CLI_AUTHENTICATION_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e

                        if [ -z "$INFRACOST_CLI_AUTHENTICATION_TOKEN" ]; then
                            echo "ERROR: Infracost credential was not injected."
                            exit 1
                        fi

                        echo "Infracost token is available."

                        infracost scan "${TF_DIR}"
                    '''
                }
            }
        }

        stage('Terraform: Init') {
            steps {
                dir("${TF_DIR}") {
                    sh '''
                        set -e
                        terraform init -reconfigure
                    '''
                }
            }
        }

        stage('Terraform: Validate') {
            steps {
                dir("${TF_DIR}") {
                    sh '''
                        set -e
                        terraform validate
                    '''
                }
            }
        }

        stage('Terraform: Plan') {
            steps {
                dir("${TF_DIR}") {
                    sh '''
                        set -e
                        terraform plan -out=tfplan
                    '''
                }
            }
        }

        stage('Terraform: Apply') {
            steps {
                dir("${TF_DIR}") {
                    sh '''
                        set -e
                        terraform apply -auto-approve tfplan
                    '''
                }
            }
        }

        stage('Get Application IP') {
            steps {
                dir("${TF_DIR}") {
                    script {
                        env.APP_PRIVATE_IP = sh(
                            script: 'terraform output -raw app_private_ip',
                            returnStdout: true
                        ).trim()

                        env.APP_PUBLIC_IP = sh(
                            script: 'terraform output -raw app_public_ip',
                            returnStdout: true
                        ).trim()
                    }

                    sh '''
                        echo "Application Private IP: ${APP_PRIVATE_IP}"
                        echo "Application Public IP: ${APP_PUBLIC_IP}"
                    '''
                }
            }
        }

        stage('Prepare Ansible Inventory') {
            steps {
                dir("${ANSIBLE_DIR}") {
                    sh '''
                        set -e

                        cat > inventory.ini <<EOF2
[app]
${APP_PRIVATE_IP} ansible_user=ubuntu ansible_ssh_private_key_file=/var/lib/jenkins/.ssh/id_rsa ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF2

                        echo "=== Generated inventory ==="
                        cat inventory.ini
                    '''
                }
            }
        }

        stage('Wait for SSH') {
            steps {
                sh '''
                    set +e

                    echo "Waiting for application server SSH..."

                    for i in $(seq 1 30); do
                        ansible all \
                            -i "${ANSIBLE_DIR}/inventory.ini" \
                            -m ping && exit 0

                        echo "SSH not ready. Attempt $i/30"
                        sleep 10
                    done

                    echo "ERROR: Application server SSH did not become available."
                    exit 1
                '''
            }
        }

        stage('Ansible: Syntax Check') {
            steps {
                dir("${ANSIBLE_DIR}") {
                    sh '''
                        set -e

                        ansible-playbook \
                            -i inventory.ini \
                            deploy.yml \
                            --syntax-check
                    '''
                }
            }
        }

        stage('Ansible: Deploy Application') {
            steps {
                dir("${ANSIBLE_DIR}") {
                    sh '''
                        set -e

                        ansible-playbook \
                            -i inventory.ini \
                            deploy.yml \
                            -e "app_source=${WORKSPACE}/application"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CloudOptima deployment completed successfully."
            echo "Application Public IP: ${APP_PUBLIC_IP}"
        }

        failure {
            echo "CloudOptima deployment failed."
        }
    }
}

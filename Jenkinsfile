pipeline {
    agent any

    parameters {
        string(
            name: 'APP_NAME',
            defaultValue: 'demo-payment-api-2',
            description: 'Name of the application to deploy'
        )

        string(
            name: 'APP_REPO_URL',
            defaultValue: '',
            description: 'Git repository URL containing the application source code'
        )
    }

    environment {
        TF_DIR = "terraform/${params.APP_NAME}"
        ANSIBLE_DIR = "ansible/${params.APP_NAME}"
        APP_DIR = "application"
    }

    stages {

        stage('Checkout Platform Repository') {
            steps {
                checkout scm
            }
        }

        stage('Validate Parameters') {
            steps {
                script {
                    if (!params.APP_REPO_URL?.trim()) {
                        error("APP_REPO_URL is required.")
                    }

                    if (!params.APP_NAME?.trim()) {
                        error("APP_NAME is required.")
                    }
                }
            }
        }

        stage('Checkout Application Source') {
            steps {
                dir("${APP_DIR}") {
                    git branch: 'main',
                        url: "${params.APP_REPO_URL}"
                }
            }
        }

        stage('Validate Application Source') {
            steps {
                sh '''
                    set -e

                    echo "===== APPLICATION SOURCE ====="
                    find "${APP_DIR}" -maxdepth 2 -type f \
                        -not -path "*/.git/*" | sort

                    echo
                    echo "===== APPLICATION SIZE ====="
                    du -sh "${APP_DIR}"
                '''
            }
        }

        stage('SecOps: IaC Scan (Checkov)') {
            steps {
                sh '''
                    checkov \
                        -d "${TF_DIR}" \
                        --soft-fail
                '''
            }
        }

        stage('SecOps: Infrastructure Vulnerability Scan (Trivy)') {
            steps {
                sh '''
                    trivy config "${TF_DIR}"
            '''
            }
        }

        stage('Infracost: Cost Estimation') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'infracost-api-key',
                        variable: 'INFRACOST_CLI_AUTHENTICATION_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e 
                        
                        echo "===== INFRACOST AUTH CHECK ====="
                        
                        if [ -z "$INFRACOST_CLI_AUTHENTICATION_TOKEN" ]; then
                        echo "ERROR: Infracost token is not available"
                        exit 1
                        fi
                        
                        echo "Infracost token: SET"

                        infracost doctor
                                               
                        echo "===== INFRACOST SCAN ====="
                        infracost scan --path "${TF_DIR}"
                    '''
                }
            }
        }

        stage('Terraform: Provision Infrastructure') {
            steps {
                dir("${TF_DIR}") {
                    sh '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }

        stage('Ansible: Configure & Deploy Application') {
            steps {
                dir("${ANSIBLE_DIR}") {
                    sh '''
                        set -e

                        echo "===== GET APPLICATION IP ====="

                        APP_IP=$(cd "${WORKSPACE}/${TF_DIR}" && \
                            terraform output -raw app_private_ip)

                        echo "Target Application Private IP: ${APP_IP}"

                        echo "Waiting for SSH service..."
                        sleep 10

                        echo "===== GENERATE ANSIBLE INVENTORY ====="

                        cat > inventory.ini <<EOF_INVENTORY
[app]
${APP_IP} ansible_user=ubuntu ansible_ssh_private_key_file=/var/lib/jenkins/.ssh/id_rsa ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF_INVENTORY

                        echo "===== TEST SSH CONNECTIVITY ====="

                        ansible \
                            all \
                            -i inventory.ini \
                            -m ping

                        echo "===== RUN ANSIBLE DEPLOYMENT ====="

                        ansible-playbook \
                            -i inventory.ini \
                            deploy.yml \
                            -e "app_source=${WORKSPACE}/${APP_DIR}"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CloudOptima deployment completed successfully.'
        }

        failure {
            echo 'CloudOptima deployment failed.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}

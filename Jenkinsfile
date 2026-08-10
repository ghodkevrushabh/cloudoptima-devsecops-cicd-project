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

                        echo "=== Infracost authentication check ==="

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
                        terraform init
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

                        cat > inventory.ini <<EOF
[all]
${APP_PRIVATE_IP} ansible_user=ubuntu ansible_ssh_private_key_file=/var/lib/jenkins/.ssh/id_rsa ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[app]
${APP_PRIVATE_IP} ansible_user=ubuntu ansible_ssh_private_key_file=/var/lib/jenkins/.ssh/id_rsa ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF

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

        stage('Deployment Verification') {
            steps {
                sh '''
                    set -e

                    echo "=== Application health check ==="

                    for i in $(seq 1 12); do
                        if curl -fsS "http://${APP_PUBLIC_IP}/" >/tmp/app_response.txt; then
                            echo "Application is responding:"
                            cat /tmp/app_response.txt
                            exit 0
                        fi

                        echo "Application not ready. Attempt $i/12"
                        sleep 5
                    done

                    echo "ERROR: Application health check failed."
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "=========================================="
            echo "CloudOptima deployment successful"
            echo "Application: ${params.APP_NAME}"
            echo "Public IP: ${env.APP_PUBLIC_IP}"
            echo "=========================================="
        }

        failure {
            echo "=========================================="
            echo "CloudOptima deployment FAILED"
            echo "Check the failed pipeline stage."
            echo "=========================================="
        }
    }
}


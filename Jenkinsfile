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

        string(
            name: 'ARTIFACT_BUCKET',
            defaultValue: 'cloudoptima-idp-artifacts-411902101270',
            description: 'S3 bucket containing generated IaC artifacts'
        )

        string(
            name: 'ARTIFACT_KEY',
            defaultValue: '',
            description: 'S3 object key of the generated IaC ZIP'
        )
    }

    environment {
        PLATFORM_TF_DIR = "terraform/platform"
        TF_DIR = "terraform/${params.APP_NAME}"
        ANSIBLE_DIR = "ansible/${params.APP_NAME}"
        ECR_REGION = "eu-north-1"
        ECR_REGISTRY = "411902101270.dkr.ecr.eu-north-1.amazonaws.com"
    }

    stages {

        stage('Checkout Infrastructure Code') {
            steps {
                checkout scm
            }
        }

        stage('Download Generated IaC Artifact') {
            steps {
                sh '''
                    set -e

                    echo "=== Generated IaC Artifact ==="

                    if [ -z "${ARTIFACT_KEY}" ]; then
                        echo "ERROR: ARTIFACT_KEY was not provided."
                        exit 1
                    fi

                    if [ -z "${ARTIFACT_BUCKET}" ]; then
                        echo "ERROR: ARTIFACT_BUCKET was not provided."
                        exit 1
                    fi

                    echo "=== Downloading generated IaC ==="

                    echo "Bucket: ${ARTIFACT_BUCKET}"
                    echo "Key: ${ARTIFACT_KEY}"

                    rm -rf artifact-package
                    mkdir -p artifact-package

                    aws s3 cp \
                        "s3://${ARTIFACT_BUCKET}/${ARTIFACT_KEY}" \
                        artifact-package/iac.zip

                    echo "=== Artifact contents ==="
                    unzip -l artifact-package/iac.zip

                    rm -rf terraform/${APP_NAME}
                    rm -rf ansible/${APP_NAME}

                    unzip -q \
                        artifact-package/iac.zip \
                        -d .

                    echo
                    echo "=== Extracted Terraform ==="
                    find "terraform/${APP_NAME}" -maxdepth 1 -type f | sort

                    echo
                    echo "=== Extracted Ansible ==="
                    find "ansible/${APP_NAME}" -maxdepth 1 -type f | sort

                    test -f "terraform/${APP_NAME}/main.tf"
                    test -f "terraform/${APP_NAME}/variables.tf"
                    test -f "terraform/${APP_NAME}/versions.tf"

                    test -f "ansible/${APP_NAME}/deploy.yml"

                    echo
                    echo "Generated IaC artifact extracted successfully."
                '''
            }
        }
        stage('Inject Platform Outputs') {
            steps {
                 script {
                     def targetGroupArn = sh(
                         script: "cd ${PLATFORM_TF_DIR} && terraform output -raw target_group_arn",
                         returnStdout: true
                     ).trim()

                     def albSecurityGroupId = sh(
                         script: "cd ${PLATFORM_TF_DIR} && terraform output -raw alb_security_group_id",
                         returnStdout: true
                     ).trim()

                     if (!targetGroupArn) {
                         error("Platform target_group_arn is empty.")
                     }

                     if (!albSecurityGroupId) {
                         error("Platform alb_security_group_id is empty.")
                     }

                     dir("${TF_DIR}") {
                         sh """
                             set -e

                             echo "=== Injecting Platform Outputs ==="

                             sed -i \
                               's|^target_group_arn *=.*|target_group_arn = "${targetGroupArn}"|' \
                               terraform.tfvars

                             sed -i \
                               's|^alb_security_group_id *=.*|alb_security_group_id = "${albSecurityGroupId}"|' \
                               terraform.tfvars

                             echo "=== Verified platform values ==="
                             grep -E 'target_group_arn|alb_security_group_id' terraform.tfvars

                             grep -q 'target_group_arn = "' terraform.tfvars
                             grep -q 'alb_security_group_id = "' terraform.tfvars 
                         """
                     }
                 }
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
                    sh '''
                        set -e

                        echo "=== Application Repository ==="
                        git remote -v
                        git branch --show-current
                        git log -1 --oneline

                        echo "=== Application Files ==="
                        find . -maxdepth 2 -type f \
                        ! -path './.git/*' \
                        ! -path './__pycache__/*' \
                        | sort

                        test -f app.py
                        test -f requirements.txt

                        echo "Application repository validation passed."
                    '''                             
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
                      sh """
                          set -e
                          echo "=== SonarQube Code Analysis ==="
                          echo "Scanner: ${scannerHome}/bin/sonar-scanner"

                          "${scannerHome}/bin/sonar-scanner" \
                            -Dsonar.projectKey=cloudoptima \
                            -Dsonar.projectName=CloudOptima \
                            -Dsonar.sources=application \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.token="\$SONAR_TOKEN" \
                            -Dsonar.scm.exclusions.disabled=true
                      """
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

        stage('Platform: Terraform') {
            steps {
                dir("${PLATFORM_TF_DIR}") {
                    sh '''
                        set -e

                        echo "=== Platform Terraform Init ==="
                        terraform init -reconfigure

                        echo "=== Platform Terraform Validate ==="
                        terraform validate

                        echo "=== Platform Terraform Plan ==="
                        terraform plan -out=platform.tfplan

                        echo "=== Platform Terraform Apply ==="
                        terraform apply -auto-approve platform.tfplan

                        echo "=== Platform Terraform Apply Complete ==="

                    '''
                }
            }
        }

        stage('Platform: Outputs') {
            steps {
                dir("${PLATFORM_TF_DIR}") {
                    script {
                        env.PLATFORM_TARGET_GROUP_ARN = sh(
                            script: 'terraform output -raw target_group_arn',
                            returnStdout: true
                    ).trim()

                        env.PLATFORM_ALB_SECURITY_GROUP_ID = sh(
                            script: 'terraform output -raw alb_security_group_id',
                            returnStdout: true
                        )
                    }

                    sh '''
                        set -e

                        echo "=== Platform Outputs ==="
                        echo "Target Group ARN: ${PLATFORM_TARGET_GROUP_ARN}"
                        echo "ALB Security Group ID: ${PLATFORM_ALB_SECURITY_GROUP_ID}"

                        test -n "${PLATFORM_TARGET_GROUP_ARN}"
                        test -n "${PLATFORM_ALB_SECURITY_GROUP_ID}"
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

        stage('Container: Build Image') {
            steps {
                script {
                    def gitSha = sh(
                        script: 'git -C application rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${gitSha}"
                    env.ECR_IMAGE = "${ECR_REGISTRY}/cloudoptima/${params.APP_NAME}:${IMAGE_TAG}"
                }

                sh '''
                    set -e

                    echo "=== Docker Build ==="
                    echo "Image tag: ${IMAGE_TAG}"
                    echo "ECR image: ${ECR_IMAGE}"

                    docker build \
                        -t "${ECR_IMAGE}" \
                        application

                    echo "Docker image built successfully."
                '''
            }
        }

        stage('SecOps: Container Image Scan - Trivy') {
            steps {
                sh '''
                    set -e

                    echo "=== Trivy Container Image Scan ==="


                    trivy image \
                        --config trivy.yaml \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        --format table \
                        "${ECR_IMAGE}"

                    echo "Container image scan passed."
                '''
            }
        }

        stage('Container: Push to ECR') {
            steps {
                sh '''
                    set -e

                    echo "=== ECR Login ==="

                    aws ecr get-login-password \
                        --region "${ECR_REGION}" | \
                    docker login \
                        --username AWS \
                        --password-stdin \
                        "${ECR_REGISTRY}"

                    echo "=== Push Image ==="

                    docker push "${ECR_IMAGE}"

                    echo "Image successfully pushed to ECR:"
                    echo "${ECR_IMAGE}"
                '''
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
                            -e "image_tag=${IMAGE_TAG}"
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

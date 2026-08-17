import os
from dotenv import load_dotenv

load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config",
        ".env"
    )
)


# ============================================================
# Environment Configuration
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AWS_REGION = os.getenv("AWS_REGION")
VPC_NAME = os.getenv("VPC_NAME")
SUBNET_ID = os.getenv("SUBNET_ID")
KEY_NAME = os.getenv("KEY_NAME")
TF_STATE_BUCKET = os.getenv("TF_STATE_BUCKET")
SSH_CIDR = os.getenv("SSH_CIDR", "10.0.0.0/16")
TARGET_GROUP_ARN = os.getenv("TARGET_GROUP_ARN")
ALB_SECURITY_GROUP_ID = os.getenv("ALB_SECURITY_GROUP_ID")

MONITORING_CIDR = os.getenv(
    "MONITORING_CIDR",
    SSH_CIDR
)

APP_INSTANCE_PROFILE = os.getenv(
    "APP_INSTANCE_PROFILE"
)

# ============================================================
# IaC Generator
# ============================================================

def generate_iac(
    app_name,
    environment,
    port,
    instance_size,
    s3_bucket_name=None
):

    base_dir = os.getenv(
    "GENERATED_BASE_DIR",
    os.path.join(BASE_DIR, "generated")
    )

    tf_dir = os.path.join(
        base_dir,
        "terraform",
        app_name
    )

    ansible_dir = os.path.join(
        base_dir,
        "ansible",
        app_name
    )

    os.makedirs(
        tf_dir,
        exist_ok=True
    )

    os.makedirs(
        ansible_dir,
        exist_ok=True
    )

    state_bucket = (
        s3_bucket_name
        or TF_STATE_BUCKET
    )

    # ========================================================
    # 1. terraform.tfvars
    # ========================================================

    tfvars_content = f'''aws_region     = "{AWS_REGION}"
app_name       = "{app_name}"
environment    = "{environment}"
app_port       = {port}
instance_type  = "{instance_size}"
vpc_name       = "{VPC_NAME}"
subnet_id      = "{SUBNET_ID}"
key_name       = "{KEY_NAME}"
ssh_cidr       = "{SSH_CIDR}"
monitoring_cidr = "{MONITORING_CIDR}"
target_group_arn = "{TARGET_GROUP_ARN}"
alb_security_group_id = "{ALB_SECURITY_GROUP_ID}"
'''

    with open(
        os.path.join(tf_dir, "terraform.tfvars"),
        "w"
    ) as f:
        f.write(tfvars_content)

    # ========================================================
    # 2. versions.tf
    # ========================================================

    versions_tf = f'''terraform {{
  required_version = ">= 1.5.0"

  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}

  backend "s3" {{
    bucket = "{state_bucket}"
    key    = "environments/{app_name}/terraform.tfstate"
    region = "{AWS_REGION}"
  }}
}}

provider "aws" {{
  region = var.aws_region
}}
'''

    with open(
        os.path.join(tf_dir, "versions.tf"),
        "w"
    ) as f:
        f.write(versions_tf)

    # ========================================================
    # 3. variables.tf
    # ========================================================

    variables_tf = '''variable "aws_region" {
  type = string
}

variable "alb_security_group_id" {
  type = string
}

variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "app_port" {
  type = number

  validation {
    condition     = var.app_port >= 1 && var.app_port <= 65535
    error_message = "Application port must be between 1 and 65535."
  }
}

variable "instance_type" {
  type = string

  validation {
    condition = contains(
      ["t3.micro", "t3.small"],
      var.instance_type
    )

    error_message = "Unsupported instance type."
  }
}

variable "vpc_name" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "key_name" {
  type = string
}

variable "ssh_cidr" {
  type = string
}

variable "monitoring_cidr" {
  type = string
}

variable "target_group_arn" {
  type = string
}
'''

    with open(
        os.path.join(tf_dir, "variables.tf"),
        "w"
    ) as f:
        f.write(variables_tf)

    # ========================================================
    # 4. main.tf
    # ========================================================

    main_tf = '''data "aws_vpc" "cloudoptima" {
  filter {
    name   = "tag:Name"
    values = [var.vpc_name]
  }
}

data "aws_subnet" "application" {
  id = var.subnet_id
}

data "aws_ssm_parameter" "ubuntu_ami" {
  name = "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
}


# ============================================================
# Application Security Group
# ============================================================

resource "aws_security_group" "app_sg" {
  name        = "${var.app_name}-sg"
  description = "Security group for ${var.app_name}"
  vpc_id      = data.aws_vpc.cloudoptima.id

  # ----------------------------------------------------------
  # Application traffic
  #
  # IMPORTANT:
  # This currently uses the configured SSH/network CIDR rather
  # than exposing the application to the entire internet.
  # ----------------------------------------------------------

  ingress {
    description = "Application traffic from CloudOptima ALB"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    security_groups = [var.alb_security_group_id]
  }

  # ----------------------------------------------------------
  # Node Exporter
  #
  # NEVER expose port 9100 publicly.
  # ----------------------------------------------------------

  ingress {
    description = "Prometheus Node Exporter from monitoring network"
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = [var.monitoring_cidr]
  }

  # ----------------------------------------------------------
  # SSH
  # ----------------------------------------------------------

  ingress {
    description = "SSH from CloudOptima network"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  # ----------------------------------------------------------
  # Outbound traffic
  # ----------------------------------------------------------
  #checkov:skip=CKV_AWS_382:Application EC2 requires outbound internet access through the private-subnet NAT Gateway for package updates, AWS APIs, and ECR image pulls.
  egress {
    description = "Outbound traffic required for package updates, AWS APIs, and ECR access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.app_name}-sg"
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}

resource "aws_kms_key" "ecr" {
  description             = "KMS key for ${var.app_name} ECR repository"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = {
    Name        = "${var.app_name}-ecr-kms"
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}

resource "aws_kms_key_policy" "ecr" {
  key_id = aws_kms_key.ecr.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid    = "EnableAccountAdministration"
        Effect = "Allow"

        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }

        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

# ============================================================
# Application ECR Repository
# ============================================================
resource "aws_ecr_repository" "app" {
  name                 = "cloudoptima/${var.app_name}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr.arn
  }

  tags = {
    Name        = "cloudoptima/${var.app_name}"
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}


# ============================================================
# Application ECR IAM Role
# ============================================================

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "app_ec2_ecr_role" {
  name = "${var.app_name}-ecr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.app_name}-ecr-role"
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}

resource "aws_iam_role_policy" "app_ec2_ecr_pull" {
  name = "${var.app_name}-ecr-pull"

  role = aws_iam_role.app_ec2_ecr_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "ecr:GetAuthorizationToken"
        ]

        Resource = "*"
      },
      {
        Effect = "Allow"

        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ]

        Resource = "arn:aws:ecr:${var.aws_region}:${data.aws_caller_identity.current.account_id}:repository/cloudoptima/${var.app_name}"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "app_ec2_profile" {
  name = "${var.app_name}-ecr-profile"
  role = aws_iam_role.app_ec2_ecr_role.name
}


# ============================================================
# Application EC2
# ============================================================

resource "aws_instance" "app_server" {

  ami           = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type = var.instance_type
  ebs_optimized = true
  subnet_id = data.aws_subnet.application.id
  monitoring = true
  vpc_security_group_ids = [
    aws_security_group.app_sg.id
  ]

  key_name = var.key_name

  # ----------------------------------------------------------
  # Security
  # ----------------------------------------------------------

  # Do not automatically expose generated application servers
  # with a public IPv4 address.
  associate_public_ip_address = false

  # ----------------------------------------------------------
  # IAM
  #
  # Only attach an instance profile when one is configured.
  # ----------------------------------------------------------

  iam_instance_profile = aws_iam_instance_profile.app_ec2_profile.name

  # ----------------------------------------------------------
  # IMDSv2
  # ----------------------------------------------------------

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "disabled"
  }

  # ----------------------------------------------------------
  # Root EBS volume
  #
  # Encrypted + gp3 instead of unencrypted gp2.
  # ----------------------------------------------------------

  root_block_device {
    encrypted   = true
    volume_type = "gp3"
    volume_size = 8

    tags = {
      Name        = "${var.app_name}-root"
      Environment = var.environment
      ManagedBy   = "CloudOptima-IDP"
    }
  }

  # ----------------------------------------------------------
  # Tags
  # ----------------------------------------------------------

  tags = {
    Name        = var.app_name
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}

resource "aws_lb_target_group_attachment" "app" {
  target_group_arn = var.target_group_arn
  target_id        = aws_instance.app_server.id
  port             = var.app_port
}

# ============================================================
# Outputs
# ============================================================

output "app_instance_id" {
  value = aws_instance.app_server.id
}

output "app_public_ip" {
  value = aws_instance.app_server.public_ip
}

output "app_private_ip" {
  value = aws_instance.app_server.private_ip
}
'''

    with open(
        os.path.join(tf_dir, "main.tf"),
        "w"
    ) as f:
        f.write(main_tf)

    # ========================================================
    # 5. Ansible Inventory
    # ========================================================

    inventory_content = '''[all]
APP_IP_PLACEHOLDER ansible_user=ubuntu

[all:vars]
ansible_python_interpreter=/usr/bin/python3
'''

    with open(
        os.path.join(ansible_dir, "inventory.ini"),
        "w"
    ) as f:
        f.write(inventory_content)

    # ========================================================
    # 6. Ansible Deployment Playbook
    # ========================================================

    playbook_content = f'''---
- name: Deploy {app_name} Application
  hosts: all
  become: true

  vars:
    app_name: "{app_name}"
    app_port: {port}
    container_port: 3000

    aws_region: "{AWS_REGION}"
    ecr_registry: "411902101270.dkr.ecr.{AWS_REGION}.amazonaws.com"
    ecr_repository: "cloudoptima/{app_name}"

    # Jenkins will provide this during deployment.
    image_tag: "latest"

  tasks:

    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true

    - name: Install required packages
      ansible.builtin.apt:
        name:
          - docker.io
          - awscli
        state: present

    - name: Ensure Docker service is running
      ansible.builtin.service:
        name: docker
        state: started
        enabled: true

    - name: Authenticate Docker to Amazon ECR
      ansible.builtin.shell: |
        aws ecr get-login-password --region {{{{ aws_region }}}} |
        docker login \
          --username AWS \
          --password-stdin \
          {{{{ ecr_registry }}}}
      args:
        executable: /bin/bash
      no_log: true

    - name: Pull application image from ECR
      community.docker.docker_image:
        name: "{{{{ ecr_registry }}}}/{{{{ ecr_repository }}}}:{{{{ image_tag }}}}"
        source: pull

    - name: Stop old application container
      community.docker.docker_container:
        name: "{{{{ app_name }}}}"
        state: absent

    - name: Run application container
      community.docker.docker_container:
        name: "{{{{ app_name }}}}"
        image: "{{{{ ecr_registry }}}}/{{{{ ecr_repository }}}}:{{{{ image_tag }}}}"
        state: started
        restart_policy: always
        published_ports:
          - "{{{{ app_port }}}}:{{{{ container_port }}}}"

    - name: Run Prometheus Node Exporter Container
      community.docker.docker_container:
        name: "node-exporter"
        image: "prom/node-exporter:latest"
        state: started
        restart_policy: always
        published_ports:
          - "9100:9100"
'''

    with open(
        os.path.join(ansible_dir, "deploy.yml"),
        "w"
    ) as f:
        f.write(playbook_content)

    # ========================================================
    # Return generated paths
    # ========================================================

    return {
        "terraform_dir": tf_dir,
        "ansible_dir": ansible_dir,
    }

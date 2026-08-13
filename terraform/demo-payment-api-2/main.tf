data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "aws_vpc" "cloudoptima" {
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

resource "aws_security_group" "app_sg" {
  name        = "${var.app_name}-sg"
  description = "Security group for ${var.app_name}"
  vpc_id      = data.aws_vpc.cloudoptima.id

  ingress {
    description = "Application traffic"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Metrics node exporter"
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  ingress {
    description = "SSH from CloudOptima network"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  egress {
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

resource "aws_iam_role" "app_ec2_ecr_role" {
  name = "${var.app_name}-ecr-pull-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "ec2.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name        = "${var.app_name}-ecr-pull-role"
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

        Resource = "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/cloudoptima/${var.app_name}"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "app_ec2_profile" {
  name = "${var.app_name}-instance-profile"
  role = aws_iam_role.app_ec2_ecr_role.name
}

resource "aws_instance" "app_server" {
  ami                         = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnet.application.id
  vpc_security_group_ids      = [aws_security_group.app_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.app_ec2_profile.name

  metadata_options {
    http_endpoint                 = "enabled"
    http_tokens                   = "required"
    http_put_response_hop_limit   = 1
  }

  tags = {
    Name        = var.app_name
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}

output "app_instance_id" { value = aws_instance.app_server.id }
output "app_public_ip" { value = aws_instance.app_server.public_ip }
output "app_private_ip" { value = aws_instance.app_server.private_ip }

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
    cidr_blocks = ["0.0.0.0/0"]
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

resource "aws_instance" "app_server" {
  ami                         = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnet.application.id
  vpc_security_group_ids      = [aws_security_group.app_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  tags = {
    Name        = var.app_name
    Environment = var.environment
    ManagedBy   = "CloudOptima-IDP"
  }
}

output "app_instance_id" { value = aws_instance.app_server.id }
output "app_public_ip" { value = aws_instance.app_server.public_ip }
output "app_private_ip" { value = aws_instance.app_server.private_ip }

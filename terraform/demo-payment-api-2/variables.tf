variable "aws_region" {
  type        = string
  description = "AWS deployment region"
}

variable "app_name" {
  type        = string
  description = "Application name"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
}

variable "app_port" {
  type        = number
  description = "Application port"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
}

variable "vpc_name" {
  type        = string
  description = "CloudOptima VPC name"
}

variable "subnet_id" {
  type        = string
  description = "Application subnet"
}

variable "key_name" {
  type        = string
  description = "EC2 key pair"
}

variable "ssh_cidr" {
  type        = string
  description = "CIDR allowed to access SSH"
}

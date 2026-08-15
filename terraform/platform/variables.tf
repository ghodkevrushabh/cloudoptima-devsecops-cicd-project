variable "aws_region" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "public_subnet_a" {
  type = string
}

variable "public_subnet_b" {
  type = string
}

variable "application_subnet_ids" {
  type = list(string)
}

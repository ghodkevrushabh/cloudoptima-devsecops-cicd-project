resource "aws_security_group" "alb" {
  name        = "cloudoptima-alb-sg"
  description = "Security group for CloudOptima public ALB"
  vpc_id      = var.vpc_id

  ingress {
    description = "Public HTTP access to CloudOptima ALB"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "cloudoptima-alb-sg"
    ManagedBy = "CloudOptima-IDP"
  }
}

resource "aws_lb" "cloudoptima" {
  name               = "cloudoptima-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets = [
    var.public_subnet_a,
    var.public_subnet_b
  ]

  tags = {
    Name      = "cloudoptima-alb"
    ManagedBy = "CloudOptima-IDP"
  }
}

resource "aws_lb_target_group" "app" {
  name        = "cloudoptima-app-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    protocol            = "HTTP"
    port                = "traffic-port"
    path                = "/"
    matcher             = "200"
    healthy_threshold   = 5
    unhealthy_threshold = 2
  }

  tags = {
    Name      = "cloudoptima-app-tg"
    ManagedBy = "CloudOptima-IDP"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.cloudoptima.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn

    forward {
      target_group {
        arn    = aws_lb_target_group.app.arn
        weight = 1
      }

    }
  }
}
output "alb_arn" {
  value = aws_lb.cloudoptima.arn
}

output "alb_dns_name" {
  value = aws_lb.cloudoptima.dns_name
}

output "alb_security_group_id" {
  value = aws_security_group.alb.id
}

output "target_group_arn" {
  value = aws_lb_target_group.app.arn
}

output "application_subnet_id" {
  value = var.application_subnet_id
}

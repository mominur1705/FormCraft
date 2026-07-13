variable "environment" {
  type    = string
  default = "dev"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "alert_email" {
  type        = string
  description = "Email for billing alerts"
}
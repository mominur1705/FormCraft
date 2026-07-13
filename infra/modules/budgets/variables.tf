variable "environment" {
  description = "dev | staging | prod"
  type        = string
}

variable "budget_limit" {
  description = "Monthly budget amount in USD"
  type        = string
  default     = "5"
}

variable "alert_email" {
  description = "Email address to send budget alerts"
  type        = string
}
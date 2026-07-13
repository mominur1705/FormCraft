terraform {
  backend "s3" {
    bucket       = "formcraft-terraform-state-53c00bcc"
    key          = "dev/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "formcraft"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

module "cognito" {
  source      = "../../modules/cognito"
  environment = var.environment
}

module "budgets" {
  source       = "../../modules/budgets"
  environment  = var.environment
  alert_email  = var.alert_email
  budget_limit = "5"
}

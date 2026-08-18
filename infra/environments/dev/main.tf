terraform {
  backend "s3" {
    bucket       = "formcraft-terraform-state-53c00bcc"
    key          = "dev/terraform.tfstate"
    region       = "us-east-1"
    dynamodb_table = "formcraft-terraform-locks"
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

data "aws_caller_identity" "current" {}

module "dynamodb" {
  source      = "../../modules/dynamodb"
  environment = var.environment
}

module "s3" {
  source      = "../../modules/s3"
  environment = var.environment
  account_id  = data.aws_caller_identity.current.account_id
}

module "iam" {
  source             = "../../modules/iam"
  environment        = var.environment
  dynamodb_table_arn = module.dynamodb.table_arn
  s3_bucket_arn      = module.s3.bucket_arn
}
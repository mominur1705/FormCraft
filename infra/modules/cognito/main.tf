# Cognito is always free up to 50,000 MAU — safe on paid account
resource "aws_cognito_user_pool" "main" {
  name = "formcraft-${var.environment}"

  password_policy {
    minimum_length    = 8
    require_uppercase = true
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
  }

  auto_verified_attributes = ["email"]

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # No advanced security features — those cost money
  # mfa_configuration = "OFF"  (default, free)

  tags = {
    Project     = "formcraft"
    Environment = var.environment
  }
}

resource "aws_cognito_user_pool_client" "app" {
  name         = "formcraft-app-${var.environment}"
  user_pool_id = aws_cognito_user_pool.main.id

  generate_secret               = false
  prevent_user_existence_errors = "ENABLED"
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  token_validity_units {
    access_token  = "minutes"
    refresh_token = "days"
  }

  access_token_validity  = 60
  refresh_token_validity = 30
}
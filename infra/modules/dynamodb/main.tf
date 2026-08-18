resource "aws_dynamodb_table" "main" {
  name         = "formcraft-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"  # free tier friendly
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "GSI1PK"
    type = "S"
  }

  attribute {
    name = "GSI1SK"
    type = "S"
  }

  # GSI: look up a form directly by formId
  global_secondary_index {
    name            = "GSI1"
    hash_key        = "GSI1PK"
    range_key       = "GSI1SK"
    projection_type = "ALL"
  }

  # 35-day point-in-time recovery — free
  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Project     = "formcraft"
    Environment = var.environment
  }
}
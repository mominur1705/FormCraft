resource "aws_s3_bucket" "uploads" {
  bucket = "formcraft-uploads-${var.environment}-${var.account_id}"

  tags = {
    Project     = "formcraft"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "uploads" {
  bucket                  = aws_s3_bucket.uploads.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_cors_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["*"]   # tighten this in prod
    max_age_seconds = 3000
  }
}

# Auto-delete uploads after 7 days in dev
resource "aws_s3_bucket_lifecycle_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  rule {
    id     = "expire-dev-uploads"
    status = "Enabled"

    expiration {
      days = 7
    }
  }
}
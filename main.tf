terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket       = "personal-prod-tofu-state"
    key          = "state"
    region       = "eu-west-2"
    use_lockfile = true
  }
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "tofu_state" {
  bucket = "personal-prod-tofu-state"
}

resource "aws_s3_bucket_versioning" "tofu_states" {
  bucket = aws_s3_bucket.tofu_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "tofu_states" {
  bucket = aws_s3_bucket.tofu_state.id
  rule {
    filter {}
    id = "main"
    noncurrent_version_expiration {
      noncurrent_days = 90
    }
    # Failed to apply - states the minimum for noncurrent_days is 30 for IA.
    #noncurrent_version_transition {
    #  noncurrent_days = 2
    #  storage_class   = "STANDARD_IA"
    #}
    noncurrent_version_transition {
      noncurrent_days = 14
      storage_class   = "GLACIER"
    }
    status = "Enabled"
  }
  depends_on = [aws_s3_bucket_versioning.tofu_states]
}

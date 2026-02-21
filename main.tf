terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket = "personal-prod-tofu-state"
    key    = "state"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
}


resource "aws_s3_bucket" "tofu-state" {
  bucket = "personal-prod-tofu-state"
}

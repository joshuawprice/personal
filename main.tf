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

# Asgard
# Add ebs disk and disk backups

# TODO: Update ssh keys
# Security groups eventually
# IPv6
resource "aws_key_pair" "muspelheim" {
  key_name   = "muspelheim"
  public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDxwpe+zdeTEZlfaUlOOoEk5Rqn7USOhXZA3X4YRozm1 josh@muspelheim"
}

data "aws_ssm_parameter" "debian_13_arm_ami" {
  name = "/aws/service/debian/release/13/latest/arm64"
}

resource "aws_instance" "asgard" {
  instance_type          = "t4g.micro"
  subnet_id              = aws_subnet.public.0.id
  vpc_security_group_ids = [aws_security_group.asgard.id]

  root_block_device {
    delete_on_termination = false
    encrypted             = true
    volume_size           = 15
  }

  ami      = data.aws_ssm_parameter.debian_13_arm_ami.insecure_value
  key_name = aws_key_pair.muspelheim.key_name
}

#resource "aws_ec2_instance_state" "stop_asgard" {
#  instance_id = aws_instance.asgard.id
#  state       = "stopped"
#  #state       = "running"
#}

data "aws_availability_zones" "available" {
  state = "available"
}

# Based on the default vpc outlined here:
# https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc-components.html
resource "aws_vpc" "main" {
  cidr_block                       = "172.20.0.0/16"
  assign_generated_ipv6_cidr_block = true
}

resource "aws_subnet" "public" {
  count                           = length(data.aws_availability_zones.available.names)
  vpc_id                          = aws_vpc.main.id
  availability_zone               = data.aws_availability_zones.available.names[count.index]
  cidr_block                      = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index)
  ipv6_cidr_block                 = cidrsubnet(aws_vpc.main.ipv6_cidr_block, 8, count.index)
  assign_ipv6_address_on_creation = true
  map_public_ip_on_launch         = true
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "asgard" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

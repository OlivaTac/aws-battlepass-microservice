// Provider configuration for AWS
provider "aws" {
  region = var.aws_region
}

// Data source to get AWS account ID
data "aws_caller_identity" "current" {}

// Locals to store common values
locals {
  aws_region     = var.aws_region
  aws_account_id = data.aws_caller_identity.current.account_id
}

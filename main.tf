// Provider configuration for AWS
provider "aws" {
  region = "ca-central-1"
}

// Data source to get AWS account ID
data "aws_caller_identity" "current" {}

// Locals to store common values
locals {
  aws_region     = "ca-central-1"
  aws_account_id = data.aws_caller_identity.current.account_id
}

# Get the AccountId
data "aws_caller_identity" "current" {}

# Get the AWS region
data "aws_region" "current" {}
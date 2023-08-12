# Get the AccountId
data "aws_caller_identity" "current" {}

# Get the AWS region
data "aws_region" "current" {}

# Get the AWS RDS DB password from Secrets Manager
data "aws_secretsmanager_secret_version" "db_creds" {
  secret_id = "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:${var.env_vars_secret_id}"
}
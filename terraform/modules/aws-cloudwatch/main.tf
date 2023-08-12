locals {
  app_name = var.app_name
}

resource "aws_cloudwatch_log_group" "ecs_migrations_log_group" {
  name              = "${local.app_name}-${var.ecs_migrations_log_group_name}"
  retention_in_days = 30
}
resource "aws_cloudwatch_log_group" "ecs_application_log_group" {
  name              = "${local.app_name}-${var.ecs_application_log_group_name}"
  retention_in_days = 30
}
output "ecs_migrations_log_group_name" {
  value = aws_cloudwatch_log_group.ecs_migrations_log_group.name
}

output "ecs_application_log_group_name" {
  value = aws_cloudwatch_log_group.ecs_application_log_group.name
}
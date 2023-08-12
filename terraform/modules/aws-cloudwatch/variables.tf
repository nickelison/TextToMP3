variable "app_name" {
  description = "Application name"
  type        = string
}

variable "ecs_migrations_log_group_name" {
  description = "CloudWatch log group name for ECS migration logs"
  type        = string
  default     = "migrations"
}

variable "ecs_application_log_group_name" {
  description = "CloudWatch log group name for ECS application logs"
  type        = string
  default     = "application"
}
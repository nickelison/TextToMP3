variable "app_name" {
  description = "Application name"
  type        = string
}

variable "aws_ecr_repository_tag_mutability" {
  description = "AWS ECR Repository Image tab mutability"
  type        = string
  default     = "MUTABLE"
}
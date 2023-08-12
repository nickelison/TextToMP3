variable "app_name" {
  description = "Application name"
  type        = string
}

variable "public_subnet_1_id" {
  description = "Public Subnet 1"
  type        = string
}

variable "ecs_sg_id" {
  description = "ECS security group"
  type        = string
}

variable "ec2_key_pair_name" {
  description = "EC2 key pair"
  type        = string
}

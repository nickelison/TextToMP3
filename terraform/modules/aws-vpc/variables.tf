variable "app_name" {
  description = "Application name"
  type        = string
}

variable "aws_vpc_cidr" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.0.0/16"
}

variable "public_subnet_1_cidr_block" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.1.0/24"
}

variable "public_subnet_2_cidr_block" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.2.0/24"
}

variable "private_subnet_1_cidr_block" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.3.0/24"
}

variable "private_subnet_2_cidr_block" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.4.0/24"
}

variable "private_subnet_3_cidr_block" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.5.0/24"
}

variable "private_subnet_4_cidr_block" {
  description = "VPC CIDR range"
  type        = string
  default     = "172.1.6.0/24"
}

variable "availability_zone_1" {
  description = "VPC CIDR range"
  type        = string
  default     = "us-east-1a"
}

variable "availability_zone_2" {
  description = "VPC CIDR range"
  type        = string
  default     = "us-east-1b"
}
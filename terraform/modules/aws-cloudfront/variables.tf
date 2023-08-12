variable "app_name" {
  description = "Application name"
  type        = string
}

variable "key_group_id" {
  description = "ID of key group to be used for CloudFront distribution"
  type        = string
}

variable "ssl_cert_arn" {
  description = "ARN of SSL certificate for domain"
  type        = string
}

variable "s3_bucket_regional_domain_name" {
  description = "The regional domain name of the S3 bucket"
  type        = string
}

variable "origin_id" {
  description = "A unique identifier for the CloudFront origin"
  type        = string
}

variable "oai_cloudfront_access_identity_path" {
  description = "The CloudFront access identity path of the Origin Access Identity"
  type        = string
}

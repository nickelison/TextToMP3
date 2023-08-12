terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.60.0"
    }
  }
}

locals {
  app_name                = "texttomp3"
  env_vars_secret_id      = "texttomp3-K5Wlga"
  cf_public_key_secret_id = "texttomp3_cloudfront_private_key-9QkgMb"
  ec2_key_pair_name       = "texttomp3"
  domain_name             = "slangz.com"
  hosted_zone_id          = "Z01813231IGMWEJEUEOC2"
  ssl_cert_arn            = "arn:aws:acm:us-east-1:431608762876:certificate/ecec5793-6687-47a7-83c8-756964dc8bb5"
  rds_availability_zone   = "us-east-1a"
  s3_static_bucket_name   = "texttomp3-django-static"
  s3_media_bucket_name    = "texttomp3-django-media"
  cloudfront_origin_id    = "texttomp3S3Origin"
  cloudfront_key_group_id = "5bb19650-39cd-4dc8-91b2-2dacf7475436"
}

module "aws-vpc" {
  source   = "./modules/aws-vpc"
  app_name = local.app_name
}

module "aws-ecr" {
  source   = "./modules/aws-ecr"
  app_name = local.app_name
}

module "aws-iam" {
  source                  = "./modules/aws-iam"
  app_name                = local.app_name
  env_vars_secret_id      = local.env_vars_secret_id
  cf_public_key_secret_id = local.cf_public_key_secret_id
}

module "aws-cloudwatch" {
  source   = "./modules/aws-cloudwatch"
  app_name = local.app_name
}

module "aws-ecs" {
  source                         = "./modules/aws-ecs"
  app_name                       = local.app_name
  ec2_key_pair_name              = local.ec2_key_pair_name
  env_vars_secret_id             = local.env_vars_secret_id
  ssl_cert_arn                   = local.ssl_cert_arn
  region                         = module.aws-iam.region
  vpc                            = module.aws-vpc.vpc_id
  public_subnet_1                = module.aws-vpc.public_subnet_1_id
  public_subnet_2                = module.aws-vpc.public_subnet_2_id
  private_subnet_1               = module.aws-vpc.private_subnet_1_id
  private_subnet_2               = module.aws-vpc.private_subnet_2_id
  ecs_service_role_arn           = module.aws-iam.ecs_service_role_arn
  ec2_role_name                  = module.aws-iam.ec2_role_name
  autoscaling_role_arn           = module.aws-iam.autoscaling_role_arn
  ecr_repo_url                   = module.aws-ecr.ecr_repo_url
  execution_role_arn             = module.aws-iam.task_execution_role_arn
  ecs_migrations_log_group_name  = module.aws-cloudwatch.ecs_migrations_log_group_name
  ecs_application_log_group_name = module.aws-cloudwatch.ecs_application_log_group_name
}

module "aws-ec2" {
  source             = "./modules/aws-ec2"
  app_name           = local.app_name
  ec2_key_pair_name  = local.ec2_key_pair_name
  public_subnet_1_id = module.aws-vpc.public_subnet_1_id
  ecs_sg_id          = module.aws-ecs.ecs_sg_id
}

module "aws-rds" {
  source                = "./modules/aws-rds/"
  app_name              = local.app_name
  env_vars_secret_id    = local.env_vars_secret_id
  rds_availability_zone = local.rds_availability_zone
  vpc_id                = module.aws-vpc.vpc_id
  ecs_sg_id             = module.aws-ecs.ecs_sg_id
  private_subnet_3_id   = module.aws-vpc.private_subnet_3_id
  private_subnet_4_id   = module.aws-vpc.private_subnet_4_id
}

module "aws-s3" {
  source             = "./modules/aws-s3"
  app_name           = local.app_name
  media_bucket_name  = local.s3_media_bucket_name
  static_bucket_name = local.s3_static_bucket_name
}

module "aws-route-53" {
  source          = "./modules/aws-route-53"
  domain_name     = local.domain_name
  hosted_zone_id  = local.hosted_zone_id
  aws_lb_dns_name = module.aws-ecs.aws_lb_dns_name
  aws_lb_zone_id  = module.aws-ecs.aws_lb_zone_id
}

module "aws-cloudfront" {
  source                              = "./modules/aws-cloudfront"
  app_name                            = local.app_name
  key_group_id                        = local.cloudfront_key_group_id
  origin_id                           = local.cloudfront_origin_id
  ssl_cert_arn                        = local.ssl_cert_arn
  s3_bucket_regional_domain_name      = module.aws-s3.media_bucket_regional_domain_name
  oai_cloudfront_access_identity_path = module.aws-s3.oai_cloudfront_access_identity_path
}

output "rds_hostname" {
  value = module.aws-rds.rds_hostname
}

output "cloudfront_domain_name" {
  value = module.aws-cloudfront.cloudfront_domain_name
}

output "ecr_repo_url" {
  value = module.aws-ecr.ecr_repo_url
}
locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
  app_name   = var.app_name
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  origin {
    domain_name = var.s3_bucket_regional_domain_name
    origin_id   = var.s3_bucket_regional_domain_name

    s3_origin_config {
      origin_access_identity = var.oai_cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.s3_bucket_regional_domain_name

    trusted_key_groups = [var.key_group_id]
    forwarded_values {
      query_string = false
      headers      = ["Origin"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  viewer_certificate {
    acm_certificate_arn      = var.ssl_cert_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  enabled         = true
  price_class     = "PriceClass_All"
  is_ipv6_enabled = true
  comment         = "${local.app_name} CloudFront distribution"
}

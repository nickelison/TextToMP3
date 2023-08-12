output "media_bucket_regional_domain_name" {
  value       = "${aws_s3_bucket.media_bucket.bucket}.s3.${aws_s3_bucket.media_bucket.region}.amazonaws.com"
  description = "The regional domain name of the S3 bucket"
}

output "static_bucket_regional_domain_name" {
  value       = "${aws_s3_bucket.media_bucket.bucket}.s3.${aws_s3_bucket.media_bucket.region}.amazonaws.com"
  description = "The regional domain name of the S3 bucket"
}

output "oai_cloudfront_access_identity_path" {
  value       = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
  description = "The CloudFront access identity path of the Origin Access Identity"
}

output "oai_iam_arn" {
  value       = aws_cloudfront_origin_access_identity.oai.iam_arn
  description = "The IAM ARN of the CloudFront Origin Access Identity"
}

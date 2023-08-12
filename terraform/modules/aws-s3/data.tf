# Get the AccountId
data "aws_caller_identity" "current" {}

# Get the AWS region
data "aws_region" "current" {}

data "aws_iam_policy_document" "media_bucket_s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.media_bucket.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.oai.iam_arn]
    }
  }
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for app"
}

resource "aws_s3_bucket" "media_bucket" {
  bucket        = var.media_bucket_name
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "media_bucket" {
  bucket              = aws_s3_bucket.media_bucket.id
  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket_policy" "media_bucket_s3_policy" {
  bucket = aws_s3_bucket.media_bucket.id
  policy = data.aws_iam_policy_document.media_bucket_s3_policy.json
}

resource "aws_s3_bucket" "static_bucket" {
  bucket        = var.static_bucket_name
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "static_bucket" {
  bucket              = aws_s3_bucket.static_bucket.id
  block_public_acls   = false
  block_public_policy = false
}

resource "aws_s3_bucket_policy" "static_bucket_s3_policy" {
  bucket = aws_s3_bucket.static_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action = [
          "s3:GetObject"
        ]
        Resource = [
          "${aws_s3_bucket.static_bucket.arn}/*"
        ]
      },
    ]
  })
}
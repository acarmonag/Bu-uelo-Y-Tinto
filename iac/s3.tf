resource "aws_s3_bucket" "config_bucket" {
  bucket_prefix = "app-config-bucket"
}

resource "aws_s3_bucket_ownership_controls" "config_bucket_ownership" {
  bucket = aws_s3_bucket.config_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "config_bucket_access" {
  bucket                  = aws_s3_bucket.config_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "docker_compose_file" {
  bucket = aws_s3_bucket.config_bucket.id
  key    = "docker-compose.yml"
  source = "${path.module}/docker-compose.yml"
  etag   = filemd5("${path.module}/docker-compose.yml")
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}
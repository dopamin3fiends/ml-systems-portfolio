provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "ml_data_bucket" {
  bucket = "ml-systems-portfolio-data"
  acl    = "private"
}

resource "aws_ec2_instance" "ml_backend_instance" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t2.micro"

  tags = {
    Name = "MLBackendInstance"
  }
}

resource "aws_lambda_function" "ml_inference_function" {
  function_name = "ml_inference"
  s3_bucket     = aws_s3_bucket.ml_data_bucket.bucket
  s3_key        = "path/to/your/lambda/package.zip"
  handler       = "inference.handler"
  runtime       = "python3.8"

  environment {
    VAR_NAME = "value"
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.ml_data_bucket.bucket
}

output "ec2_instance_id" {
  value = aws_ec2_instance.ml_backend_instance.id
}

output "lambda_function_name" {
  value = aws_lambda_function.ml_inference_function.function_name
}
# Lambda function
resource "aws_lambda_function" "api" {
  filename         = var.lambda_zip_path
  function_name    = "${var.project_name}-lambda-${var.environment}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "app.main.handler"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  runtime          = "python3.12"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  # Environment variables
  environment {
    variables = {
      USE_MOCK_AWS        = "true"
      APP_AWS_REGION      = var.aws_region
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.usage_logs.name
    }
  }

  # Tags
  tags = {
    Name        = "${var.project_name}-lambda"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.api.function_name}"
  retention_in_days = 7 # Keep logs for 7 days

  tags = {
    Name        = "${var.project_name}-lambda-logs"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
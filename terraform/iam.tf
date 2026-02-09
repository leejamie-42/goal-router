# IAM Role for Lambda execution
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role-${var.environment}"

  # Trust policy - allows Lambda to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-lambda-role"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Attach AWS managed policy for Lambda basic execution
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy for DynamoDB access
resource "aws_iam_role_policy" "dynamodb_policy" {
  name = "${var.project_name}-dynamodb-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.usage_logs.arn,
          "${aws_dynamodb_table.usage_logs.arn}/index/*"
        ]
      }
    ]
  })
}

# Custom policy for Bedrock access
resource "aws_iam_role_policy" "bedrock_policy" {
  name = "${var.project_name}-bedrock-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
        ]
      }
    ]
  })
}


# Custom policy for CloudWatch Metrics (Day 5)
resource "aws_iam_role_policy" "cloudwatch_metrics_policy" {
  name = "${var.project_name}-cloudwatch-metrics-policy"
  role = aws_iam_role.lambda_role.id

  # This policy allows the Lambda to:
  # 1. Publish custom metrics to CloudWatch
  # 2. Create log groups and streams (if they don't exist)
  # 3. Write log events to CloudWatch Logs
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData" # For custom metrics
        ]
        Resource = "*" # CloudWatch metrics don't support resource-level permissions
        Condition = {
          StringEquals = {
            "cloudwatch:namespace" = "CloudAIRouter" # Restrict to our namespace only
          }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",  # For creating log groups
          "logs:CreateLogStream", # For creating new log streams
          "logs:PutLogEvents"     # For writing logs
        ]
        Resource = [
          "arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda/${var.project_name}-*",
          "arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda/${var.project_name}-*:*"
        ]
      }
    ]
  })
}


# Cloudwatch dashboard permissions
resource "aws_iam_user_policy" "terraform_user_cloudwatch_dashboard" {
  name = "${var.project_name}-terraform-cloudwatch-dashboard"
  user = "terraform-user" # Your Terraform IAM user name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "CloudWatchDashboardManagement"
        Effect = "Allow"
        Action = [
          "cloudwatch:PutDashboard",
          "cloudwatch:GetDashboard",
          "cloudwatch:DeleteDashboards",
          "cloudwatch:ListDashboards"
        ]
        Resource = "*"
      }
    ]
  })
}
# Output the API Gateway URL
output "api_url" {
  description = "API Gateway invoke URL"
  value       = aws_apigatewayv2_stage.default.invoke_url
}

# Output the Lambda function name
output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.api.function_name
}

# Output the DynamoDB table name
output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.usage_logs.name
}

# Output the CloudWatch log group
output "lambda_log_group" {
  description = "CloudWatch log group for Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

# Output the API Gateway log group
output "api_log_group" {
  description = "CloudWatch log group for API Gateway"
  value       = aws_cloudwatch_log_group.api_logs.name
}
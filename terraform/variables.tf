# Project name - used to prefix all resources
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ai-router"
}

# AWS Region
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "ap-southeast-2"
}

# Environment (dev, staging, prod)
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# Lambda configuration
variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 300
}

variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

# Path to your Lambda deployment package
variable "lambda_zip_path" {
  description = "Path to Lambda deployment zip"
  type        = string
  default     = "../lambda-deployment.zip"
}
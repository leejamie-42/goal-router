# DynamoDB table for usage logs
resource "aws_dynamodb_table" "usage_logs" {
  name         = "${var.project_name}-usage-logs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST" # On-demand pricing (free tier friendly)
  hash_key     = "request_id"
  range_key    = "timestamp"

  # Partition key
  attribute {
    name = "request_id"
    type = "S" # String
  }

  # Sort key
  attribute {
    name = "timestamp"
    type = "S"
  }

  # Attribute for querying by date
  attribute {
    name = "date"
    type = "S"
  }

  # Global Secondary Index for querying by date
  global_secondary_index {
    name            = "date-index"
    hash_key        = "date"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  # Enable point-in-time recovery (backup)
  point_in_time_recovery {
    enabled = true
  }

  # Tags for organization
  tags = {
    Name        = "${var.project_name}-usage-logs"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
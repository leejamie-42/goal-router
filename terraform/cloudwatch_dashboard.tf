# CloudWatch Dashboard for visual monitoring
# This creates a visual dashboard in AWS Console showing key metrics at a glance

# CloudWatch Dashboard for visual monitoring

resource "aws_cloudwatch_dashboard" "main" {
  depends_on = [aws_iam_user_policy.terraform_user_cloudwatch_dashboard]

  dashboard_name = "${var.project_name}-dashboard-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [

      # -------------------------------
      # Widget 1: Request Count by Status
      # -------------------------------
      {
        type   = "metric"
        width  = 12
        height = 6
        x      = 0
        y      = 0
        properties = {
          title  = "Request Count by Status"
          region = var.aws_region
          metrics = [
            [
              "CloudAIRouter",
              "RequestCount",
              "Status", "Success",
              {
                stat  = "Sum"
                label = "Success"
                color = "#2ca02c"
              }
            ],
            [
              "CloudAIRouter",
              "RequestCount",
              "Status", "Failure",
              {
                stat  = "Sum"
                label = "Failure"
                color = "#d62728"
              }
            ]
          ]
          period  = 300
          stat    = "Sum"
          view    = "timeSeries"
          stacked = false
          yAxis = {
            left = {
              min   = 0
              label = "Request Count"
            }
          }
        }
      },

      # -------------------------------
      # Widget 2: Response Latency Percentiles
      # -------------------------------
      {
        type   = "metric"
        width  = 12
        height = 6
        x      = 12
        y      = 0
        properties = {
          title  = "Response Latency Percentiles"
          region = var.aws_region
          metrics = [
            [
              "CloudAIRouter",
              "ResponseLatency",
              "Endpoint", "/generate-plan",
              {
                stat  = "p50"
                label = "p50 (median)"
                color = "#1f77b4"
              }
            ],
            [
              "CloudAIRouter",
              "ResponseLatency",
              "Endpoint", "/generate-plan",
              {
                stat  = "p95"
                label = "p95"
                color = "#ff7f0e"
              }
            ],
            [
              "CloudAIRouter",
              "ResponseLatency",
              "Endpoint", "/generate-plan",
              {
                stat  = "p99"
                label = "p99"
                color = "#d62728"
              }
            ]
          ]
          period = 300
          view   = "timeSeries"
          yAxis = {
            left = {
              label = "Milliseconds"
              min   = 0
            }
          }
          annotations = {
            horizontal = [
              {
                label = "SLA Target (2000ms)"
                value = 2000
                color = "#d62728"
              }
            ]
          }
        }
      },

      # -------------------------------
      # Widget 3: Token Usage
      # -------------------------------
      {
        type   = "metric"
        width  = 12
        height = 6
        x      = 0
        y      = 6
        properties = {
          title  = "Token Usage (Cost Tracking)"
          region = var.aws_region
          metrics = [
            [
              "CloudAIRouter",
              "TokensUsed",
              {
                stat  = "Sum"
                label = "Total Tokens"
              }
            ]
          ]
          period = 300
          stat   = "Sum"
          view   = "timeSeries"
          yAxis = {
            left = {
              min   = 0
              label = "Token Count"
            }
          }
        }
      },

      # -------------------------------
      # Widget 4: Cost Guard Triggers
      # -------------------------------
      {
        type   = "metric"
        width  = 12
        height = 6
        x      = 12
        y      = 6
        properties = {
          title  = "Cost Guard Triggers"
          region = var.aws_region
          metrics = [
            [
              "CloudAIRouter",
              "CostGuardTriggered",
              {
                stat  = "Sum"
                label = "Requests Blocked"
                color = "#d62728"
              }
            ]
          ]
          period = 300
          stat   = "Sum"
          view   = "timeSeries"
          yAxis = {
            left = {
              min   = 0
              label = "Count"
            }
          }
        }
      },

      # -------------------------------
      # Widget 5: Requests by Category
      # -------------------------------
      {
        type   = "metric"
        width  = 12
        height = 6
        x      = 0
        y      = 12
        properties = {
          title  = "Requests by Category"
          region = var.aws_region
          metrics = [
            [
              "CloudAIRouter",
              "RequestCount",
              "Category", "certification",
              "Status", "Success",
              {
                stat  = "Sum"
                label = "Certification"
              }
            ],
            [
              "CloudAIRouter",
              "RequestCount",
              "Category", "skill-learning",
              "Status", "Success",
              {
                stat  = "Sum"
                label = "Skill Learning"
              }
            ],
            [
              "CloudAIRouter",
              "RequestCount",
              "Category", "fitness",
              "Status", "Success",
              {
                stat  = "Sum"
                label = "Fitness"
              }
            ],
            [
              "CloudAIRouter",
              "RequestCount",
              "Category", "productivity",
              "Status", "Success",
              {
                stat  = "Sum"
                label = "Productivity"
              }
            ],
            [
              "CloudAIRouter",
              "RequestCount",
              "Category", "other",
              "Status", "Success",
              {
                stat  = "Sum"
                label = "Other"
              }
            ]
          ]
          period  = 300
          stat    = "Sum"
          view    = "timeSeries"
          stacked = true
          yAxis = {
            left = {
              min   = 0
              label = "Request Count"
            }
          }
        }
      },

      # -------------------------------
      # Widget 6: Lambda Performance
      # -------------------------------
      {
        type   = "metric"
        width  = 12
        height = 6
        x      = 12
        y      = 12
        properties = {
          title  = "Lambda Invocations & Errors"
          region = var.aws_region
          metrics = [
            [
              "AWS/Lambda",
              "Invocations",
              "FunctionName", aws_lambda_function.api.function_name,
              {
                stat  = "Sum"
                label = "Invocations"
                color = "#1f77b4"
              }
            ],
            [
              "AWS/Lambda",
              "Errors",
              "FunctionName", aws_lambda_function.api.function_name,
              {
                stat  = "Sum"
                label = "Errors"
                color = "#d62728"
              }
            ],
            [
              "AWS/Lambda",
              "Throttles",
              "FunctionName", aws_lambda_function.api.function_name,
              {
                stat  = "Sum"
                label = "Throttles"
                color = "#ff7f0e"
              }
            ]
          ]
          period = 300
          view   = "timeSeries"
          yAxis = {
            left = {
              min = 0
            }
          }
        }
      }

    ]
  })
}

output "cloudwatch_dashboard_url" {
  description = "URL to CloudWatch Dashboard"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.main.dashboard_name}"
}

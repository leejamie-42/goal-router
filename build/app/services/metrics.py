import boto3
from typing import Optional
from datetime import datetime
from app.config import settings


# Publish custom metrics to CloudWatch for tracking business KPIs, setting up alarms for anomalies
class MetricsPublisher:
    def __init__(self, namespace: str = "CloudAIRouter"):
        self.cloudwatch = boto3.client("cloudwatch", region_name=settings.AWS_REGION)
        self.namespace = namespace

    def publish_token_usage(self, tokens: int, model_id: str):
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        "MetricName": "TokensUsed",
                        "Value": tokens,
                        "Unit": "Count",
                        "Timestamp": datetime.utcnow(),
                        "Dimensions": [{"Name": "ModelId", "Value": model_id}],
                    }
                ],
            )
        except Exception as e:
            print(f"Failed to publish metric: {e}")

    def publish_latency(self, latency_ms: float, endpoint: str):
        """
        Track response times

        Important for:
        - SLA monitoring
        - Performance optimization
        - User experience
        """
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        "MetricName": "ResponseLatency",
                        "Value": latency_ms,
                        "Unit": "Milliseconds",
                        "Timestamp": datetime.utcnow(),
                        "Dimensions": [{"Name": "Endpoint", "Value": endpoint}],
                    }
                ],
            )
        except Exception as e:
            print(f"Failed to publish metric: {e}")

    # Track failure/success rates
    def publish_request_count(self, success: bool, category: str):
        try:
            metric_value = 1
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        "MetricName": "RequestCount",
                        "Value": metric_value,
                        "Unit": "Count",
                        "Timestamp": datetime.utcnow(),
                        "Dimensions": [
                            {
                                "Name": "Status",
                                "Value": "Success" if success else "Failure",
                            },
                            {"Name": "Category", "Value": category or "unknown"},
                        ],
                    }
                ],
            )
        except Exception as e:
            print(f"Failed to publish metric: {e}")


metrics = MetricsPublisher()

import os


class Settings:
    # Use mock AWS clients when running locally (no credentials needed)
    USE_MOCK_AWS: bool = os.getenv("USE_MOCK_AWS", "true").lower() == "true"
    AWS_REGION: str = os.getenv(
        "APP_AWS_REGION", os.getenv("AWS_REGION", "ap-southeast-2")
    )
    DYNAMODB_TABLE_NAME: str = os.getenv("DYNAMODB_TABLE_NAME", "ai-router-usage-logs")

    # Mock responses
    MOCK_CLASSIFICATION: str = "skill-learning"


settings = Settings()

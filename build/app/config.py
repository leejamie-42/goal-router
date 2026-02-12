import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    USE_MOCK_AWS: bool = os.getenv("USE_MOCK_AWS", "false").lower() == "true"
    AWS_REGION: str = os.getenv("APP_AWS_REGION") or os.getenv("AWS_REGION") or "ap-southeast-2"
    BEDROCK_REGION: str = os.getenv("BEDROCK_REGION","us-east-1")
    DYNAMODB_TABLE_NAME: str = os.getenv("DYNAMODB_TABLE_NAME", "ai-router-usage-logs")

    MOCK_CLASSIFICATION: str = "skill-learning"

    class Config:
        populate_by_name = True
        env_file = ".env"


settings = Settings()

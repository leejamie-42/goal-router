import boto3
import json
import logging
from typing import Literal
from app.config import settings


logger = logging.getLogger(__name__)

# # initialize bedrock client
# bedrock_runtime = boto3.client(
#     service_name='bedrock-runtime',
#     region_name='ap-southeast-2'
# )

# Only create real client if not mocking
if not settings.USE_MOCK_AWS:
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name='ap-southeast-2'
    )

Category = Literal[
    "certification",
    "skill-learning",
    "fitness",
    "creative",
    "productivity",
    "other"
]

async def classify_goal(goal: str) -> str:
    """
    Classify the user's goal into a category using a small LLM call.

    This is intentionally separate from plan generation because:
    - we can use a smaller/cheaper model for classification
    - the category helps us customize the plan generation prompt
    """

    # MOCK MODE: Return fake classification for local dev
    if settings.USE_MOCK_AWS:
        logger.info("Using mock classification (local dev mode)")
        # Simple keyword-based mock classification
        goal_lower = goal.lower()
        if any(word in goal_lower for word in ['cert', 'exam', 'aws', 'test']):
            return "certification"
        elif any(word in goal_lower for word in ['exercise', 'fitness', 'gym', 'run']):
            return "fitness"
        elif any(word in goal_lower for word in ['write', 'paint', 'music', 'art']):
            return "creative"
        elif any(word in goal_lower for word in ['productivity', 'organize', 'habits']):
            return "productivity"
        else:
            return "skill-learning"


    # REAL MODE: Call Bedrock
    classification_prompt = f"""
    You are a goal classification assistant. 
    Classify the following goal into exactly one category.

    Categories:
    - certification: Preparing for a professional certification or exam
    - skill-learning: Learning a new skill (programming, language, instrument, etc.)
    - fitness: Physical health, exercise, or sports goals
    - creative: Creative pursuits (writing, art, music composition)
    - productivity: Improving work habits, time management, organization
    - other: Anything that doesn't fit above

    Goal: "{goal}"

    Respond with the category name.
    """
    try:
        # call Bedrock with Claude
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 50, 
                "messages": [
                        {
                            "role": "user",
                            "content": classification_prompt
                        }
                    ],
                    "temperature": 0.1  # for classification pick lower temperature
            })
        )

        response_body = json.loads(response['body'].read())
        category = response_body['content'][0]['text'].strip().lower()

        # valid_categories = ["certification", "skill-learning", "fitness", "creative", "productivity", "other"]
        # if category not in valid_categories:
        #     logger.warning(f"Invalid category '{category}' returned, defaulting to 'other'")
        #     category = "other"

        return category

    except Exception as e:
        logger.error(f"Error classifying goal: {str(e)}")
        return "other"


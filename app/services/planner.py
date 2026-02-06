import boto3
import json
import logging
from typing import Optional
from datetime import datetime
from app.models.schemas import (
    GeneratePlanResponse,
    WeeklyBreakdown,
    WeeklyTask,
    Resource
)

logger = logging.getLogger(__name__)

bedrock_runtime = boto3.client(
    service_name = 'bedrock-runtime',
    region_name = 'ap-southeast-2'
)

def build_system_prompt(category: str) -> str:
    """
    Build a category-specific system prompt
    """
    base_prompt="""
    You are an expert productivity coach and learning strategist.
    Your task is to create detailed, actionable plans that help people achieve their goals. 
    You must respond with a valid JSON object following this exact structure:
    {
        "estimated_duration_weeks: <number between 1-52>,

        "weekly_breakdown": [
            {  
                "week_number": 1,
                "focus_area": "<main theme for this week>",
                "tasks": [
                    {
                        "task": "<specific actionable task>",
                        "estimated_hours": <number>,
                        "milestone": <true/false>
                    }
                ]
            }
        ],

        "response": [
            {
                "title": "<resource name>",
                "url": "<URL of 'search: <term>'>",
                "resource_type": "<article/video/course/book>"
            }
        ],

        "total_estimated_hours": <number>
    }

    
    IMPORTANT:
    - Be specific and actionable
    - Break down complex goals into weekly chunks
    - Include measurable milestones
    - Suggest realistic time commitments
    - Return ONLY valid JSON, no other text
    """

    # add category-specific guidance
    category_guidance = {
        "certification": "\nFocus on: study schedules, practice exams, weak areas, exam strategies.",
        "skill-learning": "\nFocus on: progressive difficulty, deliberate practice, feedback loops.",
        "fitness": "\nFocus on: progressive overload, rest days, nutrition basics, injury prevention.",
        "creative": "\nFocus on: daily practice, skill building, feedback, finishing projects.",
        "productivity": "\nFocus on: habit formation, systems over goals, measurement, accountability."
    }

    return base_prompt + category_guidance.get(category, "")
    
    
async def generate_plan(
        goal: str,
        context: Optional[str],
        category: str,
        request_id: str
    ) -> GeneratePlanResponse:
    system_prompt = build_system_prompt(category)

    user_message = f"Goal: {goal}"

    if context:
        user_message += f"\nAdditional context: {context}"

    try:
        logger.info(f"Request {request_id}:")
        logger.info("Calling Bedrock for plan generation")

        repsonse = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',  
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7  # for more creative outputs use higher temperature
            })
        )

        response_body = json.loads(response['body'].read())
        plan_text = response_body['content'][0]['text']

        plan_json = extract_json(plan_text)

        weekly_breakdown = [
            WeeklyBreakdown(
                week_number = week['week_number'],
                focus_are = week['focus_area'],
                tasks = [WeeklyTask(**task) for task in week['tasks']]
            )
            for week in plan_json['weekly_breakdown']
        ]

        resources = [
            Resource(**resource)
            for resource in plan_json.get('resources', [])
        ]

        input_tokens = response_body.get('usage',{}).get('input_tokens',0)
        output_tokens = response_body.get('usage',{}).get('output_tokens',0)

        return GeneratePlanResponse(
            request_id=request_id,
            goal=goal,
            category=category,
            estimated_duration_weeks=plan_json['estimated_duration_weeks'],
            weekly_breakdown=weekly_breakdown,
            resources=resources,
            total_estimated_hours=plan_json['total_estimated_hours'],
            created_at=datetime.utcnow(),
            metadata={
                "tokens_used": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                },
                "model": "claude-3-sonnet"
            }
        )

    except json.JSONDecodeError as e:
        logger.error(f"Request {request_id}: Failed to parse LLM response as JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate a properly formatted plan. Please try again."
        )

    except Exception as e:
        logger.error(f"Request {request_id}: Error in plan generation: {str(e)}")
        raise
    

def extract_json(text: str) -> dict:
    # remove markdown code blocks if present
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]

    return json.loads(text.strip())
    

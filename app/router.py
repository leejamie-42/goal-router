from fastapi import APIRouter
from .models.request import GoalRequest
from .models.response import PlanResponse

router = APIRouter()

@router.post("/generate-plan", response_model=PlanResponse)
async def generate_plan(request: GoalRequest):
    return {
        "goal": request.goal,
        "category": "skill-development",
        "estimated_duration_weeks": 4,
        "weekly_breakdown": [
            {
                "week": 1,
                "focus": "Foundations",
                "tasks": ["Task 1", "Task 2"]
            }
        ],
        "resources": ["Example Resource"]
    }
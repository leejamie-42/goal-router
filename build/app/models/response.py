from pydantic import BaseModel
from typing import List


class WeeklyPlan(BaseModel):
    week: int
    focus: str
    tasks: List[str]


class PlanResponse(BaseModel):
    goal: str
    category: str
    estimated_duration_weeks: int
    weekly_breakdown: List[WeeklyPlan]
    resources: List[str]

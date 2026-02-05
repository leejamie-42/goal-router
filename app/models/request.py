from pydantic import BaseModel, Field

class GoalRequest(BaseModel):
    goal: str = Field(..., min_length=5, max_length=500)

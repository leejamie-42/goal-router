from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# This is what the user sends to our API
class GeneratePlanRequest(BaseModel):
    goal: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Additional context about the user's situation"
    )

    # example for documentation
    class Config:
        json_schema_extra = {
            "example": {
                "goal": "Improve my piano sight-reading skills",
                "context": "I'm a beginner with 6 months of practice"
            }
        }
        
# represents a single task in a week
class WeeklyTask(BaseModel):
    task: str = Field(..., description="Description of the task")
    estimated_hours: float = Field(..., gt=0, description="Time needed in hours")
    milestone: bool = Field(default=False, description="Is this a key milestone?")

# represents one week of the plan
class WeeklyBreakdown(BaseModel):
    week_number: int = Field(..., ge=1, description="Week number in the plan")
    focus_area: str = Field(..., description="Main theme/focus for this week")
    tasks: List[WeeklyTask] = Field(..., min_length=1, description="Tasks for this week")

    
# represents an external resource (article, video, etc.)
class Resource(BaseModel):
    """
    External learning resource.
    """
    title: str
    url: str
    resource_type: str = Field(..., description="Type: article, video, course, book")
    relevance_score: Optional[float] = Field(None, ge=0, le=1)


# Return: structured plan to the user
class GeneratePlanResponse(BaseModel):
    """
    Complete structured plan returned to the user.
    This is what makes our API valuable - not just text, but actionable structure.
    """
    request_id: str = Field(..., description="Unique identifier for this request")
    goal: str
    category: str = Field(..., description="Auto-classified category (e.g., skill-development)")
    estimated_duration_weeks: int = Field(..., ge=1, le=52)
    weekly_breakdown: List[WeeklyBreakdown]
    resources: List[Resource] = Field(default_factory=list)
    total_estimated_hours: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Metadata about the generation process
    metadata: dict = Field(
        default_factory=dict,
        description="Internal metadata (tokens used, cost, etc.)"
    )
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import GeneratePlanRequest, GeneratePlanResponse
from app.services.classifier import classify_goal
from app.services.planner import generate_plan
import app.services.cost_guard as cost_guard
from app.services.logger import log_request
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Plan Generation"]
)

@router.post(
    "/generate-plan", 
    response_model=GeneratePlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a structured action plan from a goal"
)

async def generate_plan_endpoint(request: GeneratePlanRequest):
    """
    Main endpoint that orchestrates the plan generation process.
    
    This function performs:
    1. Intent classification
    2. Cost estimation and guardrails
    3. Structured plan generation
    4. Usage logging
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.utcnow()

    logger.info(f"Request {request_id}: Starting plan generation", extra={
        "request_id": request_id,
        "goal_length": len(request.goal)
    })

    try:
        # classify the intent/category
        logger.info(f"Request {request_id}")
        logger.info("Classifying goal category")
        category = await classify_goal(request.goal)
        logger.info(f"Classified as '{category}'")

        # check cost limits before calling LLM - cost guardrail
        logger.info("Checking cost limits")
        estimated_tokens = cost_guard.estimate_cost(request.goal, request.context)
        cost_guard.check_cost_limits(estimated_tokens)

        # generate plan
        logger.info("Generating plan with LLM")
        plan = await generate_plan(
            goal=request.goal,
            context=request.context,
            category=category,
            request_id=request_id
        )

        # log request for observability
        end_time = datetime.utcnow()
        latency_ms = (end_time - start_time).total_seconds() * 1000

        await log_request(
            request_id=request_id,
            goal=request.goal,
            category=category,
            tokens_used=estimated_tokens,
            latency_ms=latency_ms,
            success=True
        )

        logger.info(f"Request {request_id}: Plan generated successfully", extra={
            "latency_ms": latency_ms,
            "tokens_used": estimated_tokens
        })

        return plan
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Request {request_id}: Error generating plan", extra={
            "error": str(e),
            "error_type": type(e).__name__
        })
        
        await log_request(
            request_id=request_id,
            goal=request.goal,
            category="unknown",
            tokens_used=0,
            latency_ms=0,
            success=False,
            error=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating your plan. Please try again."
        )


        

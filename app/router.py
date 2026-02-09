from fastapi import APIRouter, HTTPException, status
from app.models.schemas import GeneratePlanRequest, GeneratePlanResponse
from app.services.classifier import classify_goal
from app.services.planner import generate_plan
import app.services.cost_guard as cost_guard
from app.services.db_logger import log_request
from app.services.logger import structured_logger
from app.services.metrics import metrics
import uuid
import logging
import time
from datetime import datetime


logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Plan Generation"])


@router.post(
    "/generate-plan",
    response_model=GeneratePlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a structured action plan from a goal",
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
    start_time = time.time()

    category = None
    tokens_used = 0

    structured_logger.log_request(
        request_id=request_id, goal=request.goal, goal_length=len(request.goal)
    )

    logger.info(
        f"Request {request_id}: Starting plan generation",
        extra={"request_id": request_id, "goal_length": len(request.goal)},
    )

    try:
        # classify the intent/category
        logger.info(f"Request {request_id}")

        classification_start = time.time()
        category = await classify_goal(request.goal)
        classification_latency = (time.time() - classification_start) * 1000

        logger.info("Classifying goal category")

        category = await classify_goal(request.goal)

        logger.info(f"Classified as '{category}'")

        structured_logger.log_classification(
            request_id=request_id, category=category, latency_ms=classification_latency
        )

        # check cost limits before calling LLM - cost guardrail
        logger.info("Checking cost limits")
        tokens_used = cost_guard.estimate_cost(request.goal, request.context)
        try:
            cost_guard.check_cost_limits(tokens_used)
        except HTTPException as e:
            structured_logger.log_cost_guard_triggered(
                request_id=request_id,
                estimated_tokens=tokens_used,
                max_allowed=3000,  # Use your actual limit from cost_guard
                goal_length=len(request.goal),
            )
            metrics.publish_cost_guard_trigger()
            raise e

        # generate plan
        logger.info("Generating plan with LLM")
        plan = await generate_plan(
            goal=request.goal,
            context=request.context,
            category=category,
            request_id=request_id,
        )

        total_latency = (time.time() - start_time) * 1000

        # publish metrics to CloudWatch
        metrics.publish_latency(latency_ms=total_latency, endpoint="/generate-plan")
        metrics.publish_request_count(success=True, category=category)
        metrics.publish_token_usage(
            tokens=tokens_used,
            model_id="mock-model",  # Use actual model ID in production
        )

        # log request for observability
        await log_request(
            request_id=request_id,
            goal=request.goal,
            category=category,
            tokens_used=tokens_used,
            latency_ms=total_latency,
            success=True,
        )

        logger.info(
            f"Request {request_id}: Plan generated successfully",
            extra={"latency_ms": total_latency, "tokens_used": tokens_used},
        )

        return plan

    except HTTPException:
        raise

    except Exception as e:
        total_latency = (time.time() - start_time) * 1000

        logger.error(
            f"Request {request_id}: Error generating plan",
            extra={"error": str(e), "error_type": type(e).__name__},
        )

        structured_logger.log_error(
            request_id=request_id,
            error_type=type(e).__name__,
            error_message=str(e),
            goal_length=len(request.goal),
        )

        metrics.publish_request_count(success=False, category=category or "error")

        metrics.publish_latency(latency_ms=total_latency, endpoint="/generate-plan")

        # Log failure to DynamoDB
        await log_request(
            request_id=request_id,
            goal=request.goal,
            category=category or "unknown",
            tokens_used=0,
            latency_ms=total_latency,
            success=False,
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating your plan. Please try again.",
        )

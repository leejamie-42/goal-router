import boto3
import logging
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.config import settings
from app.services.logger import structured_logger 

logger = logging.getLogger(__name__)

if not settings.USE_MOCK_AWS:
    dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)

TABLE_NAME = settings.DYNAMODB_TABLE_NAME


async def log_request(
    request_id: str,
    goal: str,
    category: str,
    tokens_used: int,
    latency_ms: float,
    success: bool,
    error: Optional[str] = None
) -> None:
    """
    Log request details to DynamoDB for observability and cost tracking.
    
    This enables:
    - Usage analytics (how many requests per day)
    - Cost tracking (how much are we spending)
    - Performance monitoring (average latency)
    - Error tracking (what's failing)
    """
    
    # MOCK MODE: Just log to console
    if settings.USE_MOCK_AWS:
        log_entry = {
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'goal': goal[:100] + '...' if len(goal) > 100 else goal,
            'category': category,
            'tokens_used': tokens_used,
            'latency_ms': round(latency_ms, 2),
            'success': success,
        }
        if error:
            log_entry['error'] = error[:200]

        logger.info(f"[MOCK] Request logged to DynamoDB: {log_entry}")
        
        # Also use structured logger in mock mode
        structured_logger.log_llm_call(
            request_id=request_id,
            model_id="mock-model",
            input_tokens=tokens_used // 2,  # Estimate
            output_tokens=tokens_used // 2,  # Estimate
            latency_ms=latency_ms,
            success=success
        )
        return

    # REAL MODE: Log to DynamoDB
    try:
        table = dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
        
        # DynamoDB doesn't support float, use Decimal
        latency_decimal = Decimal(str(round(latency_ms, 2)))
        
        item = {
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'goal': goal[:500],  # truncate long goals
            'goal_length': len(goal),
            'category': category,
            'tokens_used': tokens_used,
            'latency_ms': latency_decimal,
            'success': success,
            'date': datetime.utcnow().strftime('%Y-%m-%d'),  # for daily aggregations
            'hour': datetime.utcnow().strftime('%Y-%m-%d-%H')  # for hourly aggregations
        }
        
        if error:
            item['error'] = error[:1000]  # truncate long errors
        
        table.put_item(Item=item)
        
        logger.info(f"Request {request_id}: Logged to DynamoDB")
        
        # Also log to CloudWatch with structured logging
        structured_logger.log_llm_call(
            request_id=request_id,
            model_id="bedrock-claude",
            input_tokens=tokens_used // 2,  # Rough estimate
            output_tokens=tokens_used // 2,
            latency_ms=latency_ms,
            success=success
        )
        
    except Exception as e:
        # Logging failures should not break the main request
        # Log the error but don't raise
        logger.error(f"Failed to log request {request_id} to DynamoDB: {str(e)}")
        
        # Use structured logger for errors
        structured_logger.log_error(
            request_id=request_id,
            error_type="DynamoDBLogError",
            error_message=str(e)
        )

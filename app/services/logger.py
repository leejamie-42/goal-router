import boto3
import logging
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.config import settings

logger = logging.getLogger(__name__)

# dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

if not settings.USE_MOCK_AWS:
    dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)

TABLE_NAME = 'ai-router-usage-logs'


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

        logger.info(f"[MOCK] Request logged: {log_entry}")
        return

    # REAL MODE: Log to DynamoDB
    try:
        table = dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
        
        # dynamoDB doesn't support float, use decimal
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
        
    except Exception as e:
        # logging failures should not break the main request
        # log the error but don't raise
        logger.error(f"Failed to log request {request_id} to DynamoDB: {str(e)}")
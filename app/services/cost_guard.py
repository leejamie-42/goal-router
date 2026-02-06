from fastapi import HTTPException, status
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# cost configuration
MAX_INPUT_TOKENS = 2000
MAX_OUTPUT_TOKENS = 4000 

COST_PER_1K_INPUT_TOKENS = 0.00025  # Claude Haiku pricing
COST_PER_1K_OUTPUT_TOKENS = 0.00125

# daily budget limit (in USD)
DAILY_BUDGET_LIMIT = 5.00


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of tokens in text.
    Rule of thumb: ~4 characters per token for English text.
    """
    if not text:
        return 0
    return len(text) // 4


def estimate_cost(goal: str, context: Optional[str] = None) -> int:
    """
    Estimate the total tokens that will be used for this request.
    
    This includes:
    - User's goal
    - Optional context
    - System prompt overhead
    - Expected output size
    
    Returns: Estimated total input tokens
    """
    goal_tokens = estimate_tokens(goal)
    context_tokens = estimate_tokens(context) if context else 0
    
    # add overhead for system prompt (our instructions to the LLM) - typically around 500-800 tokens
    system_prompt_tokens = 600
    
    total_input_tokens = goal_tokens + context_tokens + system_prompt_tokens
    
    logger.info(f"Token estimation: goal={goal_tokens}, context={context_tokens}, "
                f"system={system_prompt_tokens}, total={total_input_tokens}")
    
    return total_input_tokens


def check_cost_limits(estimated_tokens: int) -> None:
    """
    Enforce cost guardrails before making expensive LLM calls.
    Raises HTTPException if limits are exceeded.
    """
    # check if input is too large
    if estimated_tokens > MAX_INPUT_TOKENS:
        logger.warning(f"Request rejected: {estimated_tokens} tokens exceeds limit of {MAX_INPUT_TOKENS}")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "Input too large",
                "estimated_tokens": estimated_tokens,
                "max_allowed_tokens": MAX_INPUT_TOKENS,
                "message": "Please shorten your goal or context to reduce the request size."
            }
        )
    
    # estimate total cost for this request
    input_cost = (estimated_tokens / 1000) * COST_PER_1K_INPUT_TOKENS
    output_cost = (MAX_OUTPUT_TOKENS / 1000) * COST_PER_1K_OUTPUT_TOKENS
    total_cost = input_cost + output_cost
    
    logger.info(f"Estimated cost: ${total_cost:.4f} (input: ${input_cost:.4f}, output: ${output_cost:.4f})")
    
    if total_cost > 0.50:
        logger.warning(f"Request rejected: estimated cost ${total_cost:.4f} exceeds per-request limit")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "Request too expensive",
                "estimated_cost_usd": round(total_cost, 4),
                "message": "This request would be too expensive to process. Please reduce input size."
            }
        )
    
    logger.info(f"Cost check passed: ${total_cost:.4f}")
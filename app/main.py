import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StructuredLogger:

    @staticmethod
    def log_request(
        request_id: str,
        goal: str,
        goal_length: int,
        category: Optional[str] = None
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "request_received",
            "request_id": request_id,
            "goal_length": goal_length,
        }
        
        if category:
            log_entry["category"] = category
            
        logger.info(json.dumps(log_entry))
    
    @staticmethod
    def log_llm_call(
        request_id: str,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        success: bool
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "llm_call",
            "request_id": request_id,
            "model_id": model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_ms": round(latency_ms, 2),
            "success": success
        }
        logger.info(json.dumps(log_entry))
    
    @staticmethod
    def log_classification(
        request_id: str,
        category: str,
        confidence: Optional[float] = None,
        latency_ms: Optional[float] = None
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "classification",
            "request_id": request_id,
            "category": category,
        }
        
        if confidence is not None:
            log_entry["confidence"] = round(confidence, 3)
        
        if latency_ms is not None:
            log_entry["latency_ms"] = round(latency_ms, 2)
            
        logger.info(json.dumps(log_entry))
    
    @staticmethod
    def log_error(
        request_id: str,
        error_type: str,
        error_message: str,
        goal_length: Optional[int] = None,
        stack_trace: Optional[str] = None
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "error",
            "request_id": request_id,
            "error_type": error_type,
            "error_message": error_message,
        }
        
        if goal_length is not None:
            log_entry["goal_length"] = goal_length
        
        if stack_trace:
            log_entry["stack_trace"] = stack_trace[:1000]  # Truncate long traces
            
        logger.error(json.dumps(log_entry))
    
    @staticmethod
    def log_cost_guard_triggered(
        request_id: str,
        estimated_tokens: int,
        max_allowed: int,
        goal_length: int
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "cost_guard_triggered",
            "request_id": request_id,
            "estimated_tokens": estimated_tokens,
            "max_allowed_tokens": max_allowed,
            "goal_length": goal_length,
        }
        logger.warning(json.dumps(log_entry))


structured_logger = StructuredLogger()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging
from contextlib import asynccontextmanager

# configure logging to use JSON format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    This runs when the app starts and stops.
    """
    # Startup
    logger.info("Application starting up")
    logger.info("Initializing connections to AWS services")
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Application shutting down")


# create the FastAPI application
app = FastAPI(
    title="Cloud AI Personal Productivity Router",
    description="Serverless API that generates structured action plans from user goals",
    version="1.0.0",
    lifespan=lifespan
)

# # add CORS middleware (allows frontend apps to call this API)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify actual domains
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# health check endpoint (important for AWS monitoring)
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    AWS uses this to verify the Lambda is working.
    """
    return {
        "status": "healthy",
        "service": "ai-productivity-router"
    }


# root endpoint with API info
@app.get("/")
async def root():
    return {
        "service": "Cloud AI Personal Productivity Router",
        "version": "1.0.0",
        "endpoints": {
            "generate_plan": "/api/v1/generate-plan",
            "health": "/health"
        }
    }


# import and include the router
from app.router import router as api_router
app.include_router(api_router, prefix="/api/v1")


# This is the handler that AWS Lambda will call
# Mangum adapts FastAPI to work with Lambda's event format
handler = Mangum(app)
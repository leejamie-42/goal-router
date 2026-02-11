from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging
from contextlib import asynccontextmanager
import json

# configure logging to use JSON format
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    This runs when the app starts and stops.
    """
    # Startup
    startup_log = {
        "timestamp": "startup",
        "event_type": "application_startup",
        "service": "cloud-ai-router",
        "version": "1.0.0",
    }
    logger.info(json.dumps(startup_log))

    yield  # Application runs here

    # Shutdown
    shutdown_log = {
        "timestamp": "shutdown",
        "event_type": "application_shutdown",
        "service": "cloud-ai-router",
    }
    logger.info(json.dumps(shutdown_log))


# create the FastAPI application
app = FastAPI(
    title="Cloud AI Personal Productivity Router",
    description="Serverless API that generates structured action plans from user goals",
    version="1.0.0",
    lifespan=lifespan,
)

# add CORS middleware (allows frontend apps to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# health check endpoint (important for AWS monitoring)
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    AWS uses this to verify the Lambda is working.
    """
    return {"status": "healthy", "service": "ai-productivity-router"}


# root endpoint with API info
@app.get("/")
async def root():
    return {
        "service": "Cloud AI Personal Productivity Router",
        "version": "1.0.0",
        "endpoints": {"generate_plan": "/api/v1/generate-plan", "health": "/health"},
    }


# import and include the router
from app.router import router as api_router

app.include_router(api_router, prefix="/api/v1")


# This is the handler that AWS Lambda will call
# Mangum adapts FastAPI to work with Lambda's event format
handler = Mangum(app)

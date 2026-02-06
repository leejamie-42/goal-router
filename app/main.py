from fastapi import FastAPI
from mangum import Mangum
from app.router import router

app = FastAPI(
    title="Cloud AI Productivity Router",
    description="Serverless API that generates structured action plans from user input",
    version="0.1.0"
)

app.include_router(router)

handler = Mangum(app)
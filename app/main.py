from fastapi import FastAPI
from mangum import Mangum
from .router import router

app = FastAPI(
    title="Cloud AI Productivity Router",
    version="0.1.0"
)

app.include_router(router)

handler = Mangum(app)
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="HockeyVision AI",
    description="AI-powered ice hockey analysis platform",
    version="0.1.0"
)

app.include_router(router)
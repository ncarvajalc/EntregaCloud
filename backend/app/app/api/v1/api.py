from fastapi import APIRouter
from app.api.v1.endpoints import (
    weather,
    tasks
)

api_router = APIRouter()

# Include all routers
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])

#/api/tasks
api_router.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
from fastapi import APIRouter
from app.api.v1.endpoints import (
    weather,
    tasks,
    auth,
)

api_router = APIRouter()

# Include all routers
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])

#/api/tasks
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# /api/auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

from fastapi import APIRouter
from app.api.v1.endpoints import (
    tasks,
    auth,
)

api_router = APIRouter()

#/tasks
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

#/auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

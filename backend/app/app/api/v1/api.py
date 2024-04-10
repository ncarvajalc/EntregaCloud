from fastapi import APIRouter
from app.api.v1.endpoints import (
    weather,
    auth,
)

api_router = APIRouter()

# Include all routers
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])

# /api/auth/signup
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

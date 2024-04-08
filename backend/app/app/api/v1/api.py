from fastapi import APIRouter
from app.api.v1.endpoints import (
    weather,
    signup,
    login
)

api_router = APIRouter()

# Include all routers
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])

# /api/auth/signup
api_router.include_router(signup.router, prefix="/api/auth/signup", tags=["signup"])

# /api/auth/login
api_router.include_router(login.router, prefix="/api/auth/login", tags=["login"])
import shutil
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
    status,
)
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from app.core.db import create_tables
from fastapi.responses import PlainTextResponse
from celery import states
import os
from fastapi.security import OAuth2PasswordBearer


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    startup()
    yield
    shutdown()


def startup():
    print("Startup fastapi")
    print("Creating tables")
    create_tables()
    print("Tables created")


def shutdown():
    print("shutdown fastapi")


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Healthcheck endpoint
@app.get("/", response_class=PlainTextResponse, tags=["healthcheck"])
async def root():
    """
    Healthcheck for the app
    """
    return "Up and running! Visit /docs for API documentation."


# Add Routers
app.include_router(api_router_v1, prefix="/api")

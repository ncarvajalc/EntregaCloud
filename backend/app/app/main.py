from fastapi import (
    FastAPI,
)
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from app.core.db import create_tables, seed_data
from fastapi.responses import PlainTextResponse


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
    print("Seeding data")
    seed_data()
    print("Data seeded")


def shutdown():
    print("shutdown fastapi")


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

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
app.include_router(api_router_v1)

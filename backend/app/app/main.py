import shutil
from fastapi import (
    FastAPI,
    File,
    UploadFile,
)
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from app.core.db import create_tables, seed_data
from fastapi.responses import PlainTextResponse
from app.worker import celery
from celery import states
import os


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


# Upload file helper function
async def upload_file(file: UploadFile):
    file_path = f".{settings.SHARED_VOLUME_PATH}/original_files/{file.filename}"
    # Print current os path
    print(os.getcwd())

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    await file.close()
    return file_path


# Celery task test endpoint
@app.post("/edit_video", tags=["celery"])
async def edit_video(file: UploadFile = File(...)):
    """
    Celery test endpoint
    """
    file_path = await upload_file(file)
    task = celery.send_task("tasks.edit_video", args=[file_path])
    return {"task_id": task.id}


@app.get("/check/{task_id}", tags=["celery"])
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


# Add Routers
app.include_router(api_router_v1)

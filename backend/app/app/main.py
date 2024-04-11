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
from app.worker import celery
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


# Upload file helper function
async def upload_file(file: UploadFile):
    file_path = f".{settings.SHARED_VOLUME_PATH}/original_files/{file.filename}"
    # Print current os path
    print(os.getcwd())

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    await file.close()
    return file_path


def is_video_file(content_type: str) -> bool:
    allowed_mime_types = [
        "video/mp4",
        "video/avi",
        "video/mpeg",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-ms-wmv",
    ]
    return content_type in allowed_mime_types


@app.post("/edit_video", tags=["celery"])
async def edit_video(file: UploadFile = File(...)):
    """
    Celery test endpoint that only accepts video files.
    """
    if not is_video_file(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not supported. Please upload a video file.",
        )
    file_path = await upload_file(file)
    task = celery.send_task("tasks.edit_video", args=[file_path])
    return {"task_id": task.id}


@app.get("/check/{task_id}", tags=["celery"])
def check_task(task_id: str):
    """
    Check the status of a Celery task.
    """
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return res.result


# Add Routers
app.include_router(api_router_v1, prefix="/api")

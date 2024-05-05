import os
from uuid import UUID
from app.schemas.tasks import (
    FileNotFound,
    Task,
    TaskGetAll,
    TaskGetOne,
    TaskNotFound,
    TaskForbiddenDelete,
    TaskUnauthorized,
    TaskBadRequest,
    TaskSuccesfullDelete,
)
from app.services.tasks import (
    get_all_tasks,
    get_task_by_id,
    delete_task,
    create_video_task,
    update_task,
    upload_file,
    validate_is_video_file,
    download_file_from_bucket,
    clean_up_file,
)
from app.services.auth import verify_token
from app.core.db import get_db
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    status,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.config import settings
from fastapi.responses import FileResponse
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from app.worker import celery


router = APIRouter()

bearer = HTTPBearer()


@router.post(
    "",
    response_model=Task,
    responses={401: {"model": TaskUnauthorized}, 400: {"model": TaskBadRequest}},
)
async def create_task(
    file: UploadFile = File(...),
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    """
    Creates a new video editing task. User requires authorization
    """
    user_id = verify_token(auth.credentials)
    await validate_is_video_file(file)
    file_path = upload_file(file)
    celery_task = celery.send_task("tasks.edit_video", args=[file_path])
    task = create_video_task(db, file_path, celery_task.id, user_id)
    return task


@router.patch(
    "/{task_id}",
    response_model=Task,
    responses={404: {"model": TaskNotFound}, 400: {"model": TaskBadRequest}},
)
async def update_task_status(task_id: UUID, db: Session = Depends(get_db)):
    """
    Updates the status and url of a task.
    """
    return update_task(db, task_id)


@router.get(
    "",
    response_model=List[TaskGetAll],
)
async def get_tasks(
    max: Optional[int] = None,
    order: Optional[int] = None,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    """
    Retrieves all editing tasks from an authorized user in the application.
    """
    user_id = verify_token(auth.credentials)
    return get_all_tasks(db, max, order, user_id)


@router.get(
    "/{task_id}",
    response_model=TaskGetOne,
    responses={
        404: {"model": TaskNotFound},
        401: {"model": TaskUnauthorized},
        400: {"model": TaskBadRequest},
    },
)
async def get_task(
    task_id: UUID,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    """
    Retrieves information about a task in the application. The user requires authorization.
    """
    user_id = verify_token(auth.credentials)
    return get_task_by_id(db, task_id, user_id)


@router.get(
    "/{file_name}/download",
    response_class=FileResponse,
    responses={404: {"model": FileNotFound}},
)
async def download_file(
    background_tasks: BackgroundTasks,
    file_name: str,
):
    """
    Download the edited file of a task in the application.
    """
    download_file_from_bucket(file_name)
    file_path = f".{settings.SHARED_VOLUME_PATH}/edited_files/{file_name}"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    background_tasks.add_task(clean_up_file, file_path)
    return FileResponse(
        file_path, media_type="application/octet-stream", filename=file_name
    )


@router.delete(
    "/{task_id}",
    response_model=TaskSuccesfullDelete,
    responses={
        404: {"model": TaskNotFound},
        401: {"model": TaskUnauthorized},
        403: {"model": TaskForbiddenDelete},
        400: {"model": TaskBadRequest},
    },
)
async def delete_task_by_id(
    task_id: UUID,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    """
    Deletes a task in the application. The user requires authorization.
    """
    user_id = verify_token(auth.credentials)
    delete_task(db, task_id, user_id)
    return TaskSuccesfullDelete(detail="Task deleted successfully")

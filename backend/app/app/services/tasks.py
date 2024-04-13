import shutil
import os
from app.models.tasks import Task
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.core.config import settings
from uuid import UUID, uuid4

from app.models.tasks import TaskStatus


def get_all_tasks(db: Session, max: int, order: int, user_id: str):

    tasks = db.query(Task).filter(Task.user_id == user_id)

    if order:
        tasks = (
            tasks.order_by(Task.id.desc())
            if order == 1
            else tasks.order_by(Task.id.asc())
        )

    if max:
        tasks = tasks.limit(max)

    return tasks.all()


def get_task_by_id(db: Session, task_id: UUID, user_id: str):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).one_or_none()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have a task with the given id.",
        )
    return task


def create_video_task(db: Session, file_path: str, id: UUID, user_id: str):
    file_name = os.path.basename(file_path)
    
    task = Task(id=id, file_name=file_name, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: UUID):
    task_to_update = db.query(Task).filter(Task.id == task_id).first()
    if not task_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with given id not found",
        )

    task_to_update.status = TaskStatus.processed
    file_without_extension = os.path.splitext(task_to_update.file_name)[0]
    task_to_update.url = (
        f"{settings.HOST}/api/tasks/{file_without_extension}.mp4/download"
    )
    db.commit()
    db.refresh(task_to_update)
    return task_to_update


def delete_task(db: Session, task_id: UUID, user_id: str):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).one_or_none()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have a task with the given id.",
        )
    if task.status != TaskStatus.processed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The task cannot be deleted because it is being processed by the system.",
        )
    
    try :
        os.remove(f".{settings.SHARED_VOLUME_PATH}/original_files/{task.file_name}")
        os.remove(f".{settings.SHARED_VOLUME_PATH}/edited_files/{os.path.splitext(task.file_name)[0]}.mp4")
        db.delete(task)
        db.commit()
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return task


# Helper functions
async def upload_file(file: UploadFile):
    file_path = (
        f".{settings.SHARED_VOLUME_PATH}/original_files/{str(uuid4())}_{file.filename}"
    )
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    await file.close()
    return file_path


async def validate_is_video_file(file: UploadFile):
    # Check if the file is a video file
    allowed_mime_types = [
        "video/mp4",
        "video/avi",
        "video/mpeg",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-ms-wmv",
    ]

    if file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The file type is not supported. Please upload a video file.",
        )

from app.models.tasks import Task
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

def get_all_tasks(db: Session, max: int, order: int):

    tasks = db.query(Task)

    if order:
        tasks = tasks.order_by(Task.id.desc()) if order == 1 else tasks.order_by(Task.id.asc())
    
    if max:
        tasks = tasks.limit(max)

    return tasks.all()

def get_task_by_id(db: Session, task_id: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with given id not found",
        )
    return task

def create_video_task(db: Session, file: UploadFile):

    #Check if the file is a video file
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
    
    task = Task(fileName=file.filename)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: str, new_status: str):
    task_to_update = db.query(Task).filter(Task.id == task_id).first()
    if not task_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with given id not found",
        )
    
    if new_status not in ["uploaded", "processed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The status must be either 'uploaded' or 'processed'",
        )

    task_to_update.status = new_status
    if new_status == "processed":
        task_to_update.url = f'http://localhost/api/tasks/{task_id}_{task_to_update.fileName}/download'
    db.commit()
    db.refresh(task_to_update)
    return task_to_update

def delete_task(db: Session, task_id: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with given id not found",
        )
    if task.status == "uploaded":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The task cannot be deleted because it is being processed by the system.",
        )
    db.delete(task)
    db.commit()
    return task


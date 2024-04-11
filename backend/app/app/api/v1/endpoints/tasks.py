from app.schemas.tasks import Task, TaskNotFound, TaskForbiddenDelete, TaskUnauthorized, TaskBadRequest
from app.services.tasks import get_all_tasks, get_task_by_id, delete_task, create_video_task, update_task
from app.services.auth import verify_token 
from app.core.db import get_db
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.config import settings
import shutil
from fastapi.responses import FileResponse
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer


router = APIRouter()

bearer = HTTPBearer()

@router.post(
    "/",
    response_model=Task,
    responses={401: {"model": TaskUnauthorized},
               400: {"model": TaskBadRequest}},
)
async def create_task(file:UploadFile = File(...), auth: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    """
    Permite crear una nueva tarea de edición de video. El usuario requiere autorización
    """
    verify_token(auth.credentials)

    task = create_video_task(db, file)
    fileName = f"{task.id}_{file.filename}"
    file_path = f".{settings.SHARED_VOLUME_PATH}/original_files/{fileName}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    await file.close()

    #TODO: @ncarvajalc - Implementar la lógica para conectar con el worker y enviar el archivo a procesar
 
    return task

@router.patch(
    "/{task_id}",
    response_model=Task,
    responses={404: {"model": TaskNotFound},
               400: {"model": TaskBadRequest}},
)
async def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    """
    Permite actualizar el estado de una tarea en la aplicación. 
    """
    return update_task(db, task_id, status)

@router.get(
    "/",
    response_model=List[Task],
)
async def get_tasks(max:Optional[int] = None, order:Optional[int] = None, auth: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    """
    Permite recuperar todas las tareas de edición de un usuario autorizado en la aplicación.
    """
    verify_token(auth.credentials)
    return get_all_tasks(db, max, order)

@router.get(
    "/{task_id}",
    response_model=Task,
    responses={404: {"model": TaskNotFound},
               401: {"model": TaskUnauthorized}},
)
async def get_task(task_id: int, auth: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    """
    Permite recuperar la información de una tarea en la aplicación. El usuario requiere autorización.
    """
    verify_token(auth.credentials)
    return get_task_by_id(db, task_id)

@router.get(
    "/{fileName}/download",
)
async def download_file_by_id(fileName: str):
    """
    Permite descargar el archivo editado de una tarea en la aplicación. El usuario requiere autorización.
    """
    file_path = f".{settings.SHARED_VOLUME_PATH}/edited_files/{fileName}"
    # file_path = f".{settings.SHARED_VOLUME_PATH}/original_files/{fileName}"
    return FileResponse(file_path, media_type='application/octet-stream', filename=fileName)

@router.delete(
    "/{task_id}",
    response_model=Task,
    responses={404: {"model": TaskNotFound},
               401: {"model": TaskUnauthorized},
               403: {"model": TaskForbiddenDelete}},
)
async def delete_task_by_id(task_id: int, auth: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    """
    Permite eliminar una tarea en la aplicación. El usuario requiere autorización.
    """
    verify_token(auth.credentials)
    delete_task(db, task_id)
    return {"detail": "Task deleted successfully"}
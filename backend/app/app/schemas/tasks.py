from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TaskBase(BaseModel):
    id: UUID
    file_name: str
    status: str

class Task(TaskBase):
    time_stamp: datetime
    url: str

class TaskGetAll(TaskBase):
    pass

class TaskGetOne(TaskGetAll):
    url: str


class TaskNotFound(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Task with given id not found",
            }
        }


class FileNotFound(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "File not found",
            }
        }


class TaskForbiddenDelete(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "The task cannot be deleted because it is being processed by the system.",
            }
        }


class TaskUnauthorized(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "You need to be authenticated to access this endpoint",
            }
        }


class TaskBadRequest(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "The file type is not supported. Please upload a video file.",
            }
        }


class TaskSuccesfullDelete(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Task deleted successfully",
            }
        }

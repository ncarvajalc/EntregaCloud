from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    id: int
    fileName: str
    timeStamp: datetime
    status: str
    url: str
    

class Task(TaskBase):
    pass

class TaskNotFound(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Task with given id not found",
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
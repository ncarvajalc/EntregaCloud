from app.core.db import Base
from sqlalchemy import Column, String, DateTime, UUID, CheckConstraint
import datetime
from enum import Enum 
from uuid import uuid4

class TaskStatus(str, Enum):
    uploaded = "uploaded"
    processed = "processed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    time_stamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    status = Column(String, index=True, default=TaskStatus.uploaded)
    url = Column(String, default="the video is being processed")
    user_id = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(status.in_(list(TaskStatus)), name='valid_status'),
    )
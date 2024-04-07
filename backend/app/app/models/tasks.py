from app.core.db import Base
from sqlalchemy import Column, Integer, String, DateTime
import datetime


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fileName = Column(String, nullable=False)
    timeStamp = Column(DateTime, default=datetime.datetime.now())
    status = Column(String, index=True, default="uploaded")
    url = Column(String, default="the video is being processed")

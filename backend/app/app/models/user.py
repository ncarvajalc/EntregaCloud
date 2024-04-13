from app.core.db import Base
from sqlalchemy import Column, String, UUID
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password1 = Column(String, nullable=False)

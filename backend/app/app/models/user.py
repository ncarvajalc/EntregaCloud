from app.core.db import Base
from sqlalchemy import Column, String, UUID
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid4())
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password1 = Column(String, nullable=False)

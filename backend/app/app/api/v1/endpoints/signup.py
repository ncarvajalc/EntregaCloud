from app.schemas.user import UserSchema
from app.services.auth import create_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db

router = APIRouter()


@router.post("/", response_model=UserSchema)
async def create_user_endpoint(user: UserSchema, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    user_creation = create_user(db, user)
    return user_creation

from app.schemas.user import TokenData, UserSchema, UserSchemaLogin, UserSignupResponse
from app.services.auth import authenticate_user, create_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db

router = APIRouter()


@router.post("/signup", response_model=UserSignupResponse)
async def create_user_endpoint(user: UserSchema, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    user_creation = create_user(db, user)
    return user_creation


@router.post("/login", response_model=TokenData)
async def get_user_endpoint(user: UserSchemaLogin, db: Session = Depends(get_db)):
    """
    Get user by username and password
    """
    db_user = authenticate_user(user, db)
    return db_user

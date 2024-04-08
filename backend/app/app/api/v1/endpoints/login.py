from app.schemas.user import UserSchemaLogin
from app.services.auth import authenticate_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from starlette import status
router = APIRouter()

from pydantic import BaseModel
class TokenData(BaseModel):
    access_token: str
    token_type: str

@router.post("/", response_model=TokenData)
async def get_user_endpoint(user: UserSchemaLogin, db: Session = Depends(get_db)):
    """
    Get user by username and password
    """
    db_user = authenticate_user(user, db)
    return db_user

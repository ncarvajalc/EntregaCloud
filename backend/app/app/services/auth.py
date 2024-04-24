from app.models.user import User
from app.schemas.user import UserSchema, UserSchemaLogin
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
import re
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserSchema):

    # Requerimientos de la contraseña
    errors = []
    # Password requirements
    if user.password1 != user.password2:
        errors.append("Passwords do not match")
    if len(user.password1) < 8:
        errors.append("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in user.password1):
        errors.append("Password must contain a number")
    if not any(char.islower() for char in user.password1):
        errors.append("Password must contain a lower case character")
    if not any(char.isupper() for char in user.password1):
        errors.append("Password must contain an upper case character")
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=", ".join(errors),
        )

    # Raise exceptions if the email or username already exists in the database
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db_user_username = db.query(User).filter(User.username == user.username).first()
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    # Validate email format using regex
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format",
        )

    # Hash Password
    hashed_password = pwd_context.hash(user.password1)

    # Create a SQLAlchemy User model instance
    db_user = User(
        email=user.email,
        username=user.username,
        password1=hashed_password,
    )

    # Save the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(user: UserSchemaLogin, db: Session):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if db_user is None:
        return False

    if not pwd_context.verify(user.password, db_user.password1):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["sub"]
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

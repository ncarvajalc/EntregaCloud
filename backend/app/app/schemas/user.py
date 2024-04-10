from pydantic import BaseModel, validator, root_validator, ValidationError


class UserBase(BaseModel):
    email: str
    username: str
    password1: str
    password2: str


class UserSchema(UserBase):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class UserSchemaLogin(UserLogin):
    pass


class UserSignupResponse(BaseModel):
    email: str
    username: str


class TokenData(BaseModel):
    access_token: str
    token_type: str

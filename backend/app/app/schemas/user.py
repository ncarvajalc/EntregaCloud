from pydantic import BaseModel, validator, root_validator, ValidationError

class UserBase(BaseModel):
    email: str
    username: str
    password1: str
    password2: str

    # @validator('password2')
    # def passwords_match(cls, v, values, **kwargs):
    #     if 'password1' in values and v != values['password1']:
    #         raise ValidationError('Passwords do not match')
    #     return v

    # @root_validator(pre=True)
    # def remove_password2(cls, values):
    #     values.pop('password2', None)  # remove password2 from model
    #     return values

class UserSchema(UserBase):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class UserSchemaLogin(UserLogin):
    pass
from pydantic import BaseModel, EmailStr

from .roles import Roles


class BaseUser(BaseModel):
    username: str
    password: str


class LoginUser(BaseUser):
    pass


class CreateUser(BaseUser):
    email: EmailStr


class UpdateUser(BaseUser):
    email: EmailStr
    role: Roles

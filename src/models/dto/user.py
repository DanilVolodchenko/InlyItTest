from pydantic import BaseModel

from .roles import Roles


class BaseUser(BaseModel):
    username: str
    password: str


class LoginUser(BaseUser):
    pass


class CreateUser(BaseUser):
    email: str


class UpdateUser(BaseUser):
    email: str
    role: Roles


class UserToken(BaseUser):
    email: str

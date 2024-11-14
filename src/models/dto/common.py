from typing import Optional

from pydantic import BaseModel, ConfigDict

from .roles import Roles


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: Roles = Roles.user


class AdDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    user: Optional[UserDTO] = None
    comments: Optional[list['CommentDTO']] = None


class CommentDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str

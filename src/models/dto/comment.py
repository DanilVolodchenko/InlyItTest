from pydantic import BaseModel


class BaseComment(BaseModel):
    text: str


class CreateComment(BaseComment):
    pass

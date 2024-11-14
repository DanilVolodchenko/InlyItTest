from pydantic import BaseModel


class CreateToken(BaseModel):
    username: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    username: str
    role: str

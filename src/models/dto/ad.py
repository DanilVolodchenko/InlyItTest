from pydantic import BaseModel


class BaseAd(BaseModel):
    title: str
    description: str


class CreateAd(BaseAd):
    pass

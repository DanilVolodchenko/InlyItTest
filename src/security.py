from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import APIKeyCookie
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.exceptions import HTTPException

from .models.dto.security import DecodedToken, CreateToken, Token
from .config import settings
from .exceptions import NotAuthenticated


class APIKeyCookieJWT(APIKeyCookie):
    # Сделано для того, что если возникнет ошибка, то вызвать свою
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            result = await super().__call__(request)
        except HTTPException:
            raise NotAuthenticated('Пользователь не авторизован')
        return result

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token = APIKeyCookieJWT(name='access_token')


def create_access_token(data: CreateToken) -> Token:
    encoded_jwt = jwt.encode(data.model_dump(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return Token(access_token=encoded_jwt, token_type='bearer')


def get_decoded_jwt_token(token: str) -> DecodedToken:
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise JWTError('Не удалось расшифровать токен')
    return DecodedToken(**decoded_jwt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

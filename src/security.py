from fastapi.security import APIKeyCookie
from jose import JWTError, jwt
from passlib.context import CryptContext

from .models.dto.security import DecodedToken, CreateToken, Token
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token = APIKeyCookie(name='access_token')


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

from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from loguru import logger

from ..services import UserService
from ..models import session
from ..models.dto.user import LoginUser
from ..config import settings

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/login')
def login(response: Response, user: Annotated[LoginUser, Depends()], session: Annotated[Session, Depends(session)]):

    logger.info('Авторизация пользователя')
    token = UserService(session).create_token(user)
    response.set_cookie(key='access_token', value=token.access_token, max_age=settings.TOKEN_EXPIRED)
    logger.success('Пользователь успешно авторизован')
    return token


@auth_router.post('/logout', dependencies=[Depends(UserService.get_current_user)])
def logout(response: Response):

    logger.info('Разлогирование пользователя')
    response.delete_cookie(key='access_token')
    logger.success('Пользователь успешно разлогинен')

    return 'User logged out'
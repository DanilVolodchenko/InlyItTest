from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from loguru import logger

from ..models import session
from ..services import UserService
from ..models.dto.user import CreateUser
from ..models.dto.common import UserDTO
from ..utils import admin_required

user_router = APIRouter(prefix='/users', tags=['users'])


@user_router.get('/me', response_model=UserDTO)
def get_current_user(current_user: Annotated[UserDTO, Depends(UserService.get_current_user)]):
    return current_user


@user_router.get('/all', dependencies=[Depends(UserService.get_current_user)], response_model=list[UserDTO])
def get_users(session: Annotated[Session, Depends(session)]):

    logger.info('Получение всех пользователей')
    result = UserService(session).get_users()
    logger.success('Пользователи успешно получены: {}'.format(result))

    return result


@user_router.get('/{user_id:int}', dependencies=[Depends(UserService.get_current_user)], response_model=UserDTO)
def get_user_by_id(userid: Annotated[int, Path], session: Annotated[Session, Depends(session)]):

    logger.info('Получение пользователя с id={}'.format(userid))
    result = UserService(session).get_user_by_id(userid)
    logger.success('Пользователь получен: {}'.format(result))

    return result


@user_router.get('/{username:str}', dependencies=[Depends(UserService.get_current_user)])
def get_user_by_username(username: Annotated[str, Path], session: Annotated[Session, Depends(session)]):

    logger.info('Получение пользователя с username={}'.format(username))
    result = UserService(session).get_user_by_username(username)
    logger.success('Пользователь успешно получен: {}'.format(result))

    return result


@user_router.post('/create', dependencies=[Depends(UserService.get_current_user)], response_model=UserDTO)
def create_user(user: Annotated[CreateUser, Depends()], session: Annotated[Session, Depends(session)]):

    logger.info('Создание пользователя')
    result = UserService(session).create_user(user)
    logger.success('Пользователь успешно создан: {}'.format(result))

    return result


@user_router.put(
    '/{username}',
    dependencies=[Depends(UserService.get_current_user), Depends(admin_required)],
    response_model=UserDTO
)
def update_user_role(username: str, session: Annotated[Session, Depends(session)]):

    logger.info('Обновление роли пользователя')
    result = UserService(session).update_user_role(username)
    logger.success('Роль пользователя обновлена: {}'.format(result))
    return result

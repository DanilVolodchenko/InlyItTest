from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from loguru import logger

from ..models import session
from ..controllers import AdController, CommentController
from ..models.dto.ad import CreateAd
from ..models.dto.comment import CreateComment
from ..models.dto.common import UserDTO, AdDTO
from ..services import UserService, AdService, CommentService

ad_router = APIRouter(prefix='/ads', tags=['ads'])


@ad_router.get('/all', dependencies=[Depends(UserService.get_current_user)])
def get_ads(session: Annotated[Session, Depends(session)]):
    logger.info('Получение всех статей')
    result = AdController(UserService(session), AdService(session)).get_all_ads()
    logger.success('Статьи успешно получены: {}'.format(result))
    return result


@ad_router.get('/{ad_id:int}', dependencies=[Depends(UserService.get_current_user)])
def get_ad_by_id(ad_id: Annotated[int, Path], session: Annotated[Session, Depends(session)]):
    logger.info('Получение статьи по id={}'.format(ad_id))
    result = AdController(UserService(session), AdService(session)).get_by_id(ad_id)
    logger.success('Статья успешно получена: {}'.format(result))
    return result


@ad_router.post('/create', response_model=AdDTO)
def create_ad(
        ad: CreateAd,
        current_user: Annotated[UserDTO, Depends(UserService.get_current_user)],
        session: Annotated[Session, Depends(session)]
):
    logger.info('Создание статьи')
    result = AdController(UserService(session), AdService(session)).create_ad(ad, current_user.id)
    logger.success('Статья успешно создана: {}'.format(result))
    return result


@ad_router.delete('/delete/{id:int}')
def delete_ad(
        id: Annotated[int, Path],
        current_user: Annotated[UserDTO, Depends(UserService.get_current_user)],
        session: Annotated[Session, Depends(session)]
):
    logger.info('Удаление статьи с id={}'.format(id))
    result = AdController(UserService(session), AdService(session)).delete_ad(id, user=current_user)
    logger.success('Статья успешно удалена: {}'.format(result))
    return AdController(UserService(session), AdService(session)).delete_ad(id, user=current_user)


@ad_router.get('/{ad_id}/comment/all', dependencies=[Depends(UserService.get_current_user)])
def get_ad_comments(ad_id: Annotated[int, Path], session: Annotated[Session, Depends(session)]):
    logger.info('Получение комментариев для статьи с id={}'.format(ad_id))
    result = CommentController(UserService(session), AdService(session), CommentService(session)).get_comments(ad_id)
    logger.success('Комментарии успешно получены: {}'.format(result))

    return result


@ad_router.post('/{ad_id:int}/comment')
def create_comment(
        ad_id: Annotated[int, Path],
        comment: CreateComment,
        current_user: Annotated[UserDTO, Depends(UserService.get_current_user)],
        session: Annotated[Session, Depends(session)]
):
    logger.info('Создание комментария для статьи с id={}'.format(ad_id))
    result = CommentController(
        UserService(session), AdService(session), CommentService(session)
    ).create_comment(comment, current_user.id, ad_id)
    logger.success('Комментарий успешно создан: {}'.format(result))

    return result

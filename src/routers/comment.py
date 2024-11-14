from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from loguru import logger

from ..models import session
from ..services import CommentService, UserService
from ..utils import admin_required

comment_router = APIRouter(prefix='/comments', tags=['comments'])


@comment_router.delete(
    '/{comment_id}', dependencies=[Depends(UserService.get_current_user), Depends(admin_required)]
)
def delete_comment(comment_id: Annotated[int, Path], session: Annotated[Session, Depends(session)]):

    logger.info('Удаление комментария с id={}'.format(comment_id))
    result = CommentService(session).delete_comment(comment_id)
    logger.success('Комментарий успешно удален: {}'.format(result))
    return result

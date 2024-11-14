from typing import Type

from sqlalchemy.orm import Session

from .interfaces import ServiceInterface
from ..models.dto.comment import CreateComment
from ..repositories import CommentRepository
from ..models.dto.common import CommentDTO
from ..exceptions import CommentNotFound

__all__ = ['CommentService']


class CommentService(ServiceInterface[CommentRepository]):

    def __init__(self, session: Session, repository: Type[CommentRepository] = CommentRepository) -> None:
        super().__init__(session, repository)

    def get_comment_by_id(self, comment_id: int) -> CommentDTO:
        comment = self.repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound('Комментарий не найден')

        return CommentDTO.model_validate(comment)

    def create_comment(self, comment: CreateComment, user_id: int, ad_id: int) -> CommentDTO:
        comment = self.repository.create(comment, user_id=user_id, ad_id=ad_id)

        return CommentDTO.model_validate(comment)

    def get_comments(self, ad_id: int) -> list[CommentDTO]:
        comments = self.repository.get_all_by_ad_id(ad_id)

        return [CommentDTO.model_validate(comment) for comment in comments]

    def delete_comment(self, comment_id: int) -> CommentDTO:
        comment = self.repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound('Комментарий не найден')

        deleted_comment = self.repository.delete(comment)

        return CommentDTO.model_validate(deleted_comment)

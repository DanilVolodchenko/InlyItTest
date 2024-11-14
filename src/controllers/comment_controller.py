from ..models.dto.comment import CreateComment
from ..models.dto.common import CommentDTO
from ..services import UserService, AdService, CommentService

__all__ = ['CommentController']


class CommentController:
    def __init__(self, user_service: UserService, ad_service: AdService, comment_service: CommentService) -> None:
        self.user_service = user_service
        self.ad_service = ad_service
        self.comment_service = comment_service

    def create_comment(self, comment: CreateComment, user_id: int, ad_id: int) -> CommentDTO:
        user = self.user_service.get_user_by_id(user_id)
        ad = self.ad_service.get_ad_by_id(ad_id)

        return self.comment_service.create_comment(comment, user.id, ad.id)

    def get_comments(self, ad_id: int) -> list[CommentDTO]:
        ad = self.ad_service.get_ad_by_id(ad_id)

        return self.comment_service.get_comments(ad.id)

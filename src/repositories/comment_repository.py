from .interfaces import RepositoryInterface
from src.models.db.comment import Comment
from ..models.dto.comment import CreateComment

__all__ = ['CommentRepository']


class CommentRepository(RepositoryInterface[Comment]):

    def get_by_id(self, comment_id: int) -> Comment:
        return self.query.filter(self.model.id == comment_id).first()

    def create(self, comment: CreateComment, ad_id: int, user_id: int) -> Comment:
        comment = Comment(**comment.model_dump(), ad_id=ad_id, user_id=user_id)
        self.session.add(comment)
        self.session.flush()

        return comment

    def get_all_by_ad_id(self, ad_id: int) -> list[Comment]:
        return self.query.filter(self.model.ad_id == ad_id).all()

    def delete(self, comment: Comment) -> Comment:
        self.session.delete(comment)
        self.session.flush()

        return comment

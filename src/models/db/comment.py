from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from .mixins import PrimaryMixin


class Comment(PrimaryMixin, Base):
    __tablename__ = 'comments'

    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))

    user: Mapped['User'] = relationship(back_populates='comments')
    ad: Mapped['Ad'] = relationship(back_populates='comments')


from .user import User
from .ad import Ad

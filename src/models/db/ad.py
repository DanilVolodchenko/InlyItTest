from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from .mixins import PrimaryMixin


class Ad(PrimaryMixin, Base):
    __tablename__ = 'ads'

    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='ads')
    comments: Mapped[list['Comment']] = relationship(back_populates='ad')


from .user import User
from .comment import Comment

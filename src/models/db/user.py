from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from .mixins import PrimaryMixin
from ..dto.roles import Roles


class User(PrimaryMixin, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str]
    role: Mapped[Roles] = mapped_column(default=Roles.user, nullable=True)

    ads: Mapped[list['Ad']] = relationship(back_populates='user')
    comments: Mapped[list['Comment']] = relationship(back_populates='user')

    @property
    def is_admin(self):
        return self.role == Roles.admin


from .ad import Ad
from .comment import Comment

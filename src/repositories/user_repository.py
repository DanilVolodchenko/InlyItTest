from .interfaces import RepositoryInterface, T
from ..models.db.user import User

__all__ = ['UserRepository']


class UserRepository(RepositoryInterface[User]):

    def get_by_username(self, username: str) -> User:
        return self.query.filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        return self.query.filter(User.email == email).first()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()

        return user

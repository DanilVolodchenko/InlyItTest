from typing import Type, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from .interfaces import ServiceInterface
from ..models.db import User
from ..models import SessionMaker
from ..models.dto.user import CreateUser, UpdateUser, LoginUser
from ..repositories.user_repository import UserRepository
from ..models.dto.common import UserDTO
from ..models.dto.roles import Roles
from ..models.dto.security import CreateToken, Token
from ..exceptions import UserNotFound, UserFound, IncorrectPassword
from ..security import get_password_hash, get_decoded_jwt_token, verify_password, create_access_token, access_token

__all__ = ['UserService']


class UserService(ServiceInterface[UserRepository]):

    def __init__(self, session: Session, repository: Type[UserRepository] = UserRepository):
        super().__init__(session, repository)

    def get_user_by_id(self, user_id: int) -> UserDTO:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(f'Пользователь с id={user_id} не найден')

        return UserDTO.model_validate(user)

    def get_user_by_username(self, username: str) -> UserDTO:
        user = self.repository.get_by_username(username)
        if not user:
            raise UserNotFound(f'Пользователь с username={username} не найден')

        return UserDTO.model_validate(user)

    def get_user_by_email(self, email: str) -> UserDTO:
        user = self.repository.get_by_email(email)
        if not user:
            raise UserNotFound(f'Пользователь с email={email} не найден')

        return UserDTO.model_validate(user)

    def get_users(self) -> list[UserDTO]:
        users = self.repository.get_all()
        return [UserDTO.model_validate(user) for user in users]

    def create_user(self, user: CreateUser) -> UserDTO:
        user_by_username = self.repository.get_by_username(user.username)
        user_by_email = self.repository.get_by_email(user.email)
        if all([user_by_username, user_by_email]):
            raise UserFound(f'Такой пользователь уже существует')

        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, role=Roles.user, hashed_password=hashed_password)
        created_user = self.repository.create(new_user)

        return UserDTO.model_validate(created_user)

    @staticmethod
    def get_current_user(token: Annotated[str, Depends(access_token)]) -> UserDTO:

        with SessionMaker() as session:
            decoded_jwt = get_decoded_jwt_token(token)
            user = UserService(session).get_user_by_username(decoded_jwt.username)
            if not user:
                raise UserNotFound(f'Неверный токен пользователя')

            return UserDTO.model_validate(user)

    def create_token(self, user: LoginUser) -> Token:

        db_user = self.repository.get_by_username(user.username)
        if not db_user:
            raise UserNotFound(f'Пользователь не найден')

        if not verify_password(user.password, db_user.hashed_password):
            raise IncorrectPassword('Неверный логин или пароль пользователя')

        return create_access_token(CreateToken(username=db_user.username, role=db_user.role))

    def update_user_role(self, username: str) -> UserDTO:

        db_user = self.repository.get_by_username(username)
        if not db_user:
            raise UserNotFound(f'Пользователь с username={username} не найден')

        updated_user = UpdateUser(
            username=db_user.username, email=db_user.email, password=db_user.hashed_password, role=Roles.admin
        )
        new_user = self.repository.update(db_user, updated_user)

        return UserDTO.model_validate(new_user)

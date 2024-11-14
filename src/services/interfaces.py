from typing import Type, TypeVar, Generic

from sqlalchemy.orm import Session

from src.repositories.interfaces import RepositoryInterface

T = TypeVar('T', bound=RepositoryInterface)


class ServiceInterface(Generic[T]):

    def __init__(self, session: Session, repository: Type[T]) -> None:
        self.__session = session
        self.__repository = repository

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def repository(self) -> T:
        return self.__repository(self.session)

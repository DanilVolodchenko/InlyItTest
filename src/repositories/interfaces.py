from typing import Type, Optional, get_args, TypeVar, Generic

from sqlalchemy.orm import Session, Query
from pydantic import BaseModel

from src.models import Base

T = TypeVar('T', bound=Base)


class RepositoryInterface(Generic[T]):
    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def model(self) -> Type[T]:
        model_type, *_ = get_args(self.__orig_bases__[0])
        return model_type

    @property
    def query(self) -> Query:
        return self.session.query(self.model)

    def get_by_id(self, ident: int) -> Optional[T]:
        return self.query.filter(self.model.id == ident).first()

    def get_all(self) -> list[T]:
        return self.query.all()

    def update(self, item: T, new_item: BaseModel, flush: bool = False) -> T:
        for key, value in new_item.model_dump().items():
            if hasattr(item, key):
                setattr(item, key, value)

        if flush:
            self.session.flush()
        return item

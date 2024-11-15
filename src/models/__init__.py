from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = (
    settings.db_connection_string
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionMaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def session() -> Generator[Session, None, None]:
    session = SessionMaker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


from .db import User, Ad, Comment

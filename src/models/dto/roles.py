from enum import Enum


class Roles(str, Enum):
    user: str = 'user'
    admin: str = 'admin'

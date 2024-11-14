from src.models.dto.user import BaseUser


class BaseException(Exception):
    pass


class UserNotAuthenticated(BaseException):
    pass


class IncorrectToken(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class UserFound(BaseException):
    pass


class PermissionDenied(BaseException):
    pass


class AdNotFound(BaseException):
    pass


class CommentNotFound(BaseException):
    pass

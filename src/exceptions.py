class BaseInlyItException(Exception):
    pass


class UserNotAuthenticated(BaseInlyItException):
    pass


class IncorrectToken(BaseInlyItException):
    pass


class UserNotFound(BaseInlyItException):
    pass


class UserFound(BaseInlyItException):
    pass


class PermissionDenied(BaseInlyItException):
    pass


class AdNotFound(BaseInlyItException):
    pass


class CommentNotFound(BaseInlyItException):
    pass

from src.core.abc.exceptions import BaseException


class UserNotFoundException(BaseException):
    detail = "User not found"

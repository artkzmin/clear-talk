from src.core.abc.exceptions import BaseException


class UserNotFoundException(BaseException):
    detail = "User not found"


class UserAlreadyExistsException(BaseException):
    detail = "User already exists"

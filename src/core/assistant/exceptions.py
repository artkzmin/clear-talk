from src.core.abc.exceptions import BaseException


class AssistantClientException(BaseException):
    detail = "Assistant client exception"


class MessagesMustNotBeEmptyException(BaseException):
    detail = "Messages must not be empty"


class FirstMessageMustBeFromSystemException(BaseException):
    detail = "First message must be from system"


class InvalidSenderException(BaseException):
    detail = "Invalid sender at position"

from src.core.abc.exceptions import BaseException


class LastMessageSenderRepeatsException(BaseException):
    detail = "Last message sender repeats"


class CannotCreateSystemMessageException(BaseException):
    detail = "Cannot create system message"


class FirstMessageMustBeFromSystemException(BaseException):
    detail = "First message must be from system"

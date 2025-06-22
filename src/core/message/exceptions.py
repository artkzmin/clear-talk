from src.core.abc.exceptions import BaseException
from src.core.message.enums import MessageSenderType


class LastMessageSenderRepeatsException(BaseException):
    detail = "Last message sender repeats"
    sender: MessageSenderType


class CannotCreateSystemMessageException(BaseException):
    detail = "Cannot create system message"


class FirstMessageMustBeFromSystemException(BaseException):
    detail = "First message must be from system"

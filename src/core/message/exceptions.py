from src.core.abc.exceptions import BaseException
from src.core.message.enums import MessageSenderType


class LastMessageSenderRepeatsException(BaseException):
    detail = "Last message sender repeats"
    sender_type: MessageSenderType


class CannotCreateSystemMessageException(BaseException):
    detail = "Cannot create system message"

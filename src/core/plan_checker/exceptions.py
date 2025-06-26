from src.core.abc.exceptions import BaseException


class PlanNotActiveException(BaseException):
    detail = "Plan expired"


class PlanMessagesCountLimitException(BaseException):
    detail = "Plan messages count limit"


class PlanTokensLimitException(BaseException):
    detail = "Plan tokens limit"

from src.core.abc.exceptions import BaseException


class ActiveUserPlanNotFoundException(BaseException):
    detail = "Active user plan not found"


class PlanNotFoundException(BaseException):
    detail = "Plan not found"


class UserPlanExceededLimitException(BaseException):
    detail = "User plan exceeded limit"


class UserPlanExceededContextTokensException(BaseException):
    detail = "User plan exceeded context tokens"

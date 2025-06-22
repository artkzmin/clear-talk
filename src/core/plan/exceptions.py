from src.core.abc.exceptions import BaseException


class PlanNotFoundException(BaseException):
    detail = "Plan not found"

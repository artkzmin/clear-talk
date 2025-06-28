from enum import StrEnum


class ModeType(StrEnum):
    TEST = "TEST"
    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


class ServiceType(StrEnum):
    TELEGRAM = "TELEGRAM"
    API = "API"

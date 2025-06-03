from src.core.entities.base import BaseEntityStrID
from src.core.entities.plan import Plan


class User(BaseEntityStrID):
    plan: Plan

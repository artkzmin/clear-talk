from src.persistence.mappers.base import BaseMapper
from src.persistence.models.user import UserModel
from src.core.user.entities import User


class UserMapper(BaseMapper[UserModel, User]):
    entity_type = User
    model_type = UserModel

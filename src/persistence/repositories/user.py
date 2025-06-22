from uuid import UUID
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from src.core.user.entities import User
from src.core.user.interfaces import UserRepositoryInterface
from src.core.user.exceptions import UserAlreadyExistsException

from src.persistence.mappers.user import UserMapper
from src.persistence.repositories.base import BaseRepository
from src.persistence.models.user import UserModel

from src.infrastructure.logger import logger_app

logger = logger_app.getChild(__name__)


class UserRepository(
    BaseRepository[UserModel, User, UserMapper], UserRepositoryInterface
):
    model = UserModel
    entity = User
    mapper = UserMapper

    async def create_user(self, user: User) -> UUID:
        try:
            user = await self.create(entity=user)
        except IntegrityError as e:
            logger.error(e)
            raise UserAlreadyExistsException()
        return user.id

    async def is_user_exists(self, hashed_external_user_id: str) -> bool:
        stmt = select(
            exists().where(UserModel.hashed_external_id == hashed_external_user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_by_external_id(
        self, hashed_external_user_id: str
    ) -> User | None:
        return await self.get_one_or_none(
            UserModel.hashed_external_id == hashed_external_user_id
        )

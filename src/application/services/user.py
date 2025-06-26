from src.core.user.services import UserService
from src.core.user.entities import InputUser, User
from src.core.user.enums import ExternalServiceType
from src.persistence.storage import inject_storage, Storage
from src.infrastructure.utils.hasher import HmacSha256Hasher


@inject_storage
async def get_or_create_telegram_user(telegram_user_id: int, storage: Storage) -> User:
    return await UserService(
        storage=storage, hasher_utility=HmacSha256Hasher()
    ).get_or_create_external_user(
        InputUser(
            external_id=str(telegram_user_id),
            external_service=ExternalServiceType.TELEGRAM,
        )
    )


@inject_storage
async def get_telegram_user(telegram_user_id: int, storage: Storage) -> User:
    """
    Raises:
        src.core.user.exceptions.UserNotFoundException:
            If the user is not found.
    """
    return await UserService(
        storage=storage, hasher_utility=HmacSha256Hasher()
    ).get_user_by_external_id(
        InputUser(
            external_id=str(telegram_user_id),
            external_service=ExternalServiceType.TELEGRAM,
        )
    )

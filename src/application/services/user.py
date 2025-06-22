from src.core.user.services import UserService
from src.core.user.entities import InputUser, User
from src.core.user.enums import ExternalServiceType
from src.persistence.storage import inject_storage, Storage
from src.infrastructure.utils.hasher import HmacSha256Hasher
from src.infrastructure.utils.encryptor import FernetEncryptorUtility


@inject_storage
async def get_or_create_telegram_user(telegram_user_id: int, storage: Storage) -> User:
    return await UserService(
        storage=storage,
        hasher=HmacSha256Hasher(),
        encryptor=FernetEncryptorUtility(),
    ).get_or_create_user(
        InputUser(
            external_id=str(telegram_user_id),
            external_service=ExternalServiceType.TELEGRAM,
        )
    )

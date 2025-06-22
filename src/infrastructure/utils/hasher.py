import hmac
import hashlib
from src.infrastructure.config import settings
from src.core.interfaces import HasherUtilityInterface


class HmacSha256Hasher(HasherUtilityInterface):
    def __init__(self):
        self._secret_key = settings.security.hash_key.encode("utf-8")

    def get_hash(self, string: str) -> str:
        return hmac.new(
            self._secret_key, string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

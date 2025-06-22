from cryptography.fernet import Fernet

from src.core.interfaces import EncryptorUtilityInterface
from src.infrastructure.config import settings


class FernetEncryptorUtility(EncryptorUtilityInterface):
    def __init__(self):
        self._fernet = Fernet(settings.security.encrypt_key.encode())

    def encrypt(self, plaintext: str) -> str:
        encrypted = self._fernet.encrypt(plaintext.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_data: str) -> str:
        decrypted = self._fernet.decrypt(encrypted_data.encode())
        return decrypted.decode()

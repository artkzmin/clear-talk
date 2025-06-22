from typing import Protocol, runtime_checkable

from src.core.plan.interfaces import PlanRepositoryInterface
from src.core.user.interfaces import UserRepositoryInterface
from src.core.message.interfaces import MessageRepositoryInterface
from src.core.abc.interfaces import SessionInterface


@runtime_checkable
class SessionMakerProtocol(Protocol):
    def __call__(self, **kwargs) -> SessionInterface: ...


@runtime_checkable
class StorageInterface(Protocol):
    session: SessionInterface

    @property
    def plan(self) -> PlanRepositoryInterface: ...

    @property
    def user(self) -> UserRepositoryInterface: ...

    @property
    def message(self) -> MessageRepositoryInterface: ...

    def __init__(self, session_factory: SessionMakerProtocol) -> None: ...

    async def __aenter__(self) -> "StorageInterface": ...

    async def __aexit__(self, *args) -> None: ...

    async def commit(self) -> None: ...


@runtime_checkable
class EncryptorUtilityInterface(Protocol):
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts the given plaintext string and returns a base64-encoded string.
        """

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts the given base64-encoded encrypted string
        and returns the original plaintext.
        """


@runtime_checkable
class HasherUtilityInterface(Protocol):
    def get_hash(self, string: str) -> str: ...

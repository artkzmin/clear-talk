from src.persistence.mappers.base import BaseMapper
from src.persistence.models.message import MessageModel
from src.core.message.entities import EncryptedMessage


class MessageMapper(BaseMapper[MessageModel, EncryptedMessage]):
    entity_type = EncryptedMessage
    model_type = MessageModel

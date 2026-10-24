import logging

from aiogram.types import Message

from core.application.chat_service import ChatService
from core.domain.chat import ChatType

log = logging.getLogger(__name__)


def message_log(
    message: Message,
    sender: str | None = None,
    recipient: str | None = None,
    chat_service: ChatService | None = None,
) -> None:
    if sender is None:
        sender = message.from_user.username if message.from_user else None

    if recipient is None:
        recipient = message.chat.username if message.chat.username != sender else None

    if chat_service is not None:
        if recipient is None:
            chat = chat_service.get_chat(message.chat.id)
            if chat is not None:
                
                if chat.type == ChatType.PRIVATE:
                    recipient = "bot"
                    
                elif chat.type == ChatType.BUSINESS:
                    if message.from_user is not None:
                        other = chat.get_other_user(message.from_user.id)
                        recipient = other.username if other is not None else None
                        
                else:
                    recipient = f"{message.chat.title} ({chat.type.value})" if message.chat.title else f"<{chat.type.value}>"
                    
    elif message.business_connection_id is not None:
        log.warning("chat_service missing for business message logger")

    sender_str = sender or "?"
    recipient_str = recipient or "?"
    
    text = message.text or f"<{message.content_type}>"
    log.info("[%s -> %s]: %s", sender_str, recipient_str, text)
    

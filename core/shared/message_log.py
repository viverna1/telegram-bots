from aiogram.types import Message

from core.application.chat_service import ChatService


def log(
    message: Message,
    sender: str | None = None,
    recipient: str | None = None,
    chat_service: ChatService | None = None,
) -> None:
    if sender is None:
        sender = message.from_user.username if message.from_user else None

    if recipient is None:
        recipient = message.chat.username if message.chat.username != sender else None
    
    if recipient is None and chat_service is not None and message.from_user is not None:
        chat = chat_service.get_chat(message.chat.id)
        if chat is not None and len(chat.users) == 2:
            other = next(
                (u for u in chat.users if u.id != message.from_user.id),
                None,
            )
            recipient = other.username if other is not None else None

    sender_str = sender or "?"
    recipient_str = recipient or "?"
    target = "?" if sender_str == recipient_str else recipient_str

    text = message.text or f"<{message.content_type}>"
    print(f"[{sender_str}] -> [{target}]: {text}")
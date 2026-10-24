from aiogram.types import Message

    
def log(message: Message, sender: str | None = None, recipient: str | None = None) -> None:
    if sender is None:
        sender = message.from_user.username if message.from_user else '?'
    if recipient is None:
        recipient = message.chat.username if message.chat else '?'

    if recipient is None or sender == recipient:
        print(f"[{sender}] -> [?]: {message.text}")
    else:
        print(f"[{sender}] -> [{recipient}]: {message.text}")

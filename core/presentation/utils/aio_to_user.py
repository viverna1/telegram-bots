from datetime import datetime

from aiogram.types import User as AiogramUser

from core.domain.user import User


def aio_to_user(aio_user: AiogramUser) -> User:
    return User(
        id=aio_user.id,
        username=aio_user.username,
        first_name=aio_user.first_name,
        registered_at=datetime.now(),
    )

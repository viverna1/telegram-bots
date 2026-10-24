## Run

```bash
py run.py               # показать список ботов
py run.py <bot_number>  # запустить бота с номером <bot_number>
```

## Usage

В src должен быть `main.py`:
```python
from core.presentation.bot import Bot

from .handlers import router


def main():
    bot = Bot(router)
    bot.run()


if __name__ == "__main__":
    main()
```

В `handlers.py`:
```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.presentation.handlers import base_start

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await base_start(message)
```

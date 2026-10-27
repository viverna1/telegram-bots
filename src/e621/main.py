import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot as AioBot
from aiogram import html

from core.presentation.bot import Bot

from .config_repository import ConfigRepository
from .e621_posts import E621Posts
from .handlers import router

CONFIG_PATH = Path(__file__).parent / "config.json"

log = logging.getLogger(__name__)


async def send_post(
    bot: AioBot,
    chat_id: int,
    e621_posts: E621Posts,
) -> None:
    try:
        post = await e621_posts.get_good_post()
        if post is None:
            log.info("no new post")
        else:
            link = e621_posts.get_link(post)
            await bot.send_message(chat_id, html.link("post", link))
            e621_posts.mark_post_as_sent(post["id"])
            log.info("sent post id=%s", post["id"])
    except asyncio.CancelledError:
        log.info("send_post_loop cancelled")
        raise
    except Exception:
        log.exception("send_post_loop iteration failed")


async def main() -> None:
    config_repository = ConfigRepository(str(CONFIG_PATH))
    e621_posts = E621Posts(config_repository)

    bot = Bot(router, on_shutdown=[e621_posts.aclose], e621_posts=e621_posts)
    # bot.run()

    await send_post(bot._bot, -1003793977933, e621_posts)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

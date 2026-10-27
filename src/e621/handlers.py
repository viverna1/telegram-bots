from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message

from core.presentation.handlers import base_start

from .e621_posts import E621Posts

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    base_start(message)
    await message.answer("e621")


@router.message(Command("get"))
async def cmd_get(message: Message, e621_posts: E621Posts):
    post = await e621_posts.get_good_post()
    if post is not None:
        e621_posts.mark_post_as_sent(post["id"])
        answer = f"{html.link('post', e621_posts.get_link(post))}"
        await message.answer(answer)
        print("sent post:", post["id"])
    else:
        await message.answer("no posts")
        print("no sent post")

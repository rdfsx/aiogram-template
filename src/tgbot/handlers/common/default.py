from aiogram import Router
from aiogram.types import Message

from src.tgbot.models import UserModel


async def get_default_message(m: Message, user: UserModel):
    await m.answer(str(user), parse_mode=None)


def setup(router: Router):
    router.message.register(get_default_message)

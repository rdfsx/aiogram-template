from aiogram import Bot, Router
from aiogram.types import Message


async def get_start_message(m: Message, bot: Bot):
    await m.answer("Hello")


def setup(router: Router):
    router.message.register(get_start_message, commands="start")

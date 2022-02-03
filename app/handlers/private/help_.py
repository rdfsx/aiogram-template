from aiogram import Dispatcher
from aiogram.types import Message


async def get_help_message(m: Message):
    await m.answer("This is a bot")


def setup(dp: Dispatcher):
    dp.message.register(get_help_message, commands="help")

from aiogram import Dispatcher
from aiogram.types import Message


async def get_help_message(m: Message):
    await m.answer("Это бот.")


def setup(dp: Dispatcher):
    dp.register_message_handler(get_help_message, commands="help")

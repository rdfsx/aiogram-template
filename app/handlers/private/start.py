from aiogram import Dispatcher
from aiogram.types import Message


async def get_start_message(m: Message):
    await m.answer('Hello')


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")

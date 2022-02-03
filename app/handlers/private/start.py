from aiogram import Dispatcher
from aiogram.types import Message


async def get_start_message(m: Message):
    await m.answer('Hello')


def setup(dp: Dispatcher):
    dp.message.register(get_start_message, commands="start")

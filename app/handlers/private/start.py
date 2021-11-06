from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel


async def get_start_message(m: Message):
    await m.answer(f"Привет, {m.from_user.first_name}!")


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")

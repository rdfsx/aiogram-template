from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel


async def get_help_message(m: Message, user: UserModel):
    await m.answer("This is a bot")


def setup(dp: Dispatcher):
    dp.register_message_handler(get_help_message, commands="help")

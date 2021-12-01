from typing import Callable

from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel


async def get_help_message(m: Message, i18n: Callable, user: UserModel):
    await m.answer(i18n("locale.help"))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_help_message, commands="help")

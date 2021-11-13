import functools
import types
from typing import Callable

from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel


async def get_start_message(m: Message, i18n: Callable):
    await m.answer(i18n("locale.start"))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")

import types

from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel


async def get_start_message(m: Message, i18n: types.ModuleType):
    await m.answer(i18n.t("locale.start"))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")

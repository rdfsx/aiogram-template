from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel


async def get_default_message(m: Message, user: UserModel):
    await m.answer(str(user), parse_mode=None)


def setup(dp: Dispatcher):
    dp.message.register(get_default_message)

from aiogram import Dispatcher, html
from aiogram.types import Message

from app.models import UserModel


async def get_default_message(m: Message, user: UserModel):
    await m.answer(html.quote(user))


def setup(dp: Dispatcher):
    dp.message.register(get_default_message)

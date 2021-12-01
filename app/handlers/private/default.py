from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import quote_html

from app.models import UserModel


async def get_default_message(m: Message, user: UserModel):
    await m.answer(quote_html(user))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_default_message)

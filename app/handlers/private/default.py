import asyncio

from aiogram import Dispatcher
from aiogram.types import Message

from app.models import UserModel
from app.utils.misc.lock_decorator import lock_up


@lock_up()
async def get_default_message(m: Message, user: UserModel):
    await m.answer("Start")
    await asyncio.sleep(10)
    await m.answer(str(user), parse_mode=None)


def setup(dp: Dispatcher):
    dp.message.register(get_default_message)

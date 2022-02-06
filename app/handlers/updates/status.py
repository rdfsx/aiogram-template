from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated

from app.models import UserModel


async def set_my_status(my_chat_member: ChatMemberUpdated, user: UserModel):
    user.status = my_chat_member.new_chat_member.status
    await user.save()


def setup(dp: Dispatcher):
    dp.my_chat_member.register(set_my_status)

from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated

from app.models import UserModel


async def set_my_status(my_chat_member: ChatMemberUpdated):
    user = await UserModel.find_one(UserModel.id == my_chat_member.from_user.id)
    if user:
        user.status = my_chat_member.new_chat_member.status
        await user.save()


def setup(dp: Dispatcher):
    dp.register_my_chat_member_handler(set_my_status)

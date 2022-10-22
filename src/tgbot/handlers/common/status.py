from aiogram import Router
from aiogram.types import ChatMemberUpdated

from src.tgbot.models import UserModel


async def set_my_status(my_chat_member: ChatMemberUpdated, user: UserModel):
    user.status = my_chat_member.new_chat_member.status
    await user.save()


def setup(router: Router):
    router.my_chat_member.register(set_my_status)

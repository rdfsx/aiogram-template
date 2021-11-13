from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated
from odmantic import AIOEngine

from app.models import UserModel


async def set_status(my_chat_member: ChatMemberUpdated, db: AIOEngine, user: UserModel):
    user.status = my_chat_member.new_chat_member.status
    await db.save(user)


def setup(dp: Dispatcher):
    dp.register_my_chat_member_handler(set_status)

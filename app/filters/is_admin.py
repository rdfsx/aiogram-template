from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.config import Config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return str(message.from_user.id) in Config.ADMINS

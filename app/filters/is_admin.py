from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from app.config import Config


class AdminFilter(BaseFilter):

    async def __call__(self, event_from_user: types.User) -> bool:
        return str(event_from_user.id) in Config.ADMINS

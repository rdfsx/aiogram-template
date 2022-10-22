from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from src.tgbot.config import Config


class AdminFilter(BaseFilter):
    async def __call__(self, obj: TelegramObject, event_from_user: types.User) -> bool:
        return str(event_from_user.id) in Config.ADMINS

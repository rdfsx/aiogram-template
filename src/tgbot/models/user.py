from enum import Enum
from typing import Optional

from aiogram import Bot
from beanie import Insert, after_event
from pydantic import Field

from src.tgbot.config import Config
from src.tgbot.models.base import TimeBaseModel
from src.tgbot.utils.broadcasting import broadcast, from_iterable


class UserRoles(str, Enum):
    new = "new"
    user = "user"
    admin = "admin"


class UserModel(TimeBaseModel):
    id: int = Field(...)
    language: str = "en"
    real_language: str = "en"
    role: UserRoles = Field(default=UserRoles.new)
    status: str = "member"
    username: Optional[str] = Field(default=None)

    class Settings:
        name = "Users"

    @after_event(Insert)
    async def notify_admins_new_user(self):
        async with Bot(token=Config.BOT_TOKEN).context() as bot:
            pics = await bot.get_user_profile_photos(self.id)
            txt = [
                "#new_user",
                f'id: <a href="tg://user?id={self.id}">{self.id}</a>',
                f"username: @{self.username}",
            ]
            photo = None
            if pics and pics.total_count > 0:
                photo = pics.photos[0][-1].file_id

            admins = from_iterable(Config.ADMINS)

            if photo:
                return await broadcast(
                    admins, bot.send_photo, False, photo=photo, caption="\n".join(txt)
                )
            return await broadcast(admins, bot.send_message, False, text="\n".join(txt))

from typing import Optional

from aiogram import Bot, html
from beanie import Insert, after_event
from pydantic import Field

from src.tgbot.config import Config
from src.tgbot.models.base import TimeBaseModel
from src.tgbot.utils.broadcasting import broadcast, from_iterable


class ChatModel(TimeBaseModel):
    id: int = Field(...)
    type: str = Field(...)
    username: Optional[str] = Field(default=None)

    class Settings:
        name = "Chats"

    @after_event(Insert)
    async def notify_admins_new_chat(self):
        if self.type != "private":
            async with Bot(token=Config.BOT_TOKEN).context() as bot:
                chat = await bot.get_chat(chat_id=self.id)
                return await broadcast(
                    from_iterable(Config.ADMINS),
                    bot.send_message,
                    False,
                    text="\n".join(
                        [
                            "#new_group",
                            f"Full name: {html.quote(chat.first_name)}",
                            f"id: {chat.id}",
                            f"Title: {chat.title}",
                            f"Description: {chat.description}",
                            f"Members: {await bot.get_chat_member_count(chat.id)}",
                            f"username: @{chat.username}",
                        ]
                    ),
                )

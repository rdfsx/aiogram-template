import asyncio
import datetime
import logging
from typing import Literal

from aiogram import Bot
from aiogram.types import Chat, User

from src.tgbot.config import Config
from src.tgbot.utils.requests_utils import send_request

logger = logging.getLogger(__name__)


async def log_stat(  # TODO: need refactoring
    bot: Bot,
    time: datetime.datetime,
    user: User | None = None,
    chat: Chat | None = None,
    event: str | None = None,
    error: str | None = None,
    error_msg: str | None = None,
    action: Literal["new_user", "new_chat", "new_bot", "interaction", "error"] = "interaction",
) -> None:
    data = {
        "client_id": str(user.id if user else None),
        "user_id": str(user.id if user else None),
        "events": [
            {
                "name": event,
                "params": {
                    "language": user.language_code if user else None,
                    "username": user.username if user else None,
                    "full_name": user.full_name if user else None,
                    "chat_type": chat.type if chat else None,
                    "bot_username": (await bot.me()).username,
                    "engagement_time_msec": "10",
                },
            }
        ],
    }
    try:
        asyncio.create_task(
            send_request(
                Config.GA_API_URI,
                method="POST",
                response_type="text",
                json=data,
                headers={
                    "host": "www.google-analytics.com",
                    "content-type": "application/json",
                },
            )
        )
    except Exception as e:
        logger.error(f"Stats error: {e}")

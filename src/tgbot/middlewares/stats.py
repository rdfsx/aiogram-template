import datetime
from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware, Bot, types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import Chat, User

from src.tgbot.utils.analytics import log_stat


class StatsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data["handler"]
        user: Optional[User] = data.get("event_from_user")
        chat: Optional[Chat] = data.get("event_chat")
        bot: Bot = data["bot"]

        if not user:
            return await handler(event, data)

        result = await handler(event, data)

        await log_stat(
            bot,
            datetime.datetime.utcnow(),
            user,
            chat,
            real_handler.callback.__name__,
        )

        return result

from typing import Callable, Awaitable, Any, cast

from aiogram import BaseMiddleware, Bot
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import TelegramObject


class EventLockMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data["handler"]
        bot: Bot = cast(Bot, data["bot"])
        state: FSMContext = data["state"]

        lock = hasattr(real_handler.callback, "lock")

        if not lock:
            return await handler(event, data)

        async with state.storage.lock(bot=bot, key=state.key):
            return await handler(event, data)

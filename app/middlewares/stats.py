import datetime
from typing import Callable, Any, Awaitable, Optional

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import User
from aioinflux import InfluxDBClient

from app.utils.analytics import log_stat


class StatsMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data["handler"]
        influx_client: InfluxDBClient = data["influx_client"]
        user: Optional[User] = data.get("event_from_user")

        if not user:
            return await handler(event, data)

        result = await handler(event, data)

        await log_stat(influx_client, user, datetime.datetime.now(), real_handler.callback.__name__)

        return result

from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from aioinflux import InfluxDBClient


class InfluxDBMiddleware(BaseMiddleware):

    def __init__(self, influx_client: InfluxDBClient):
        self.influx_client = influx_client
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        data["influx_client"] = self.influx_client

        return await handler(event, data)

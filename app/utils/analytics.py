import datetime
import logging

from aiogram.types import User
from aioinflux import InfluxDBWriteError, InfluxDBClient


async def log_stat(
        client: InfluxDBClient,
        user: User,
        time: datetime.datetime,
        event: str = None,
        error: str = None) -> None:
    data = {
        "measurement": "bot_statistics",
        "timestamp": time.timestamp(),
        "fields": {"event": 1},
        "tags": {
            'username': user.username,
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language_code': user.language_code,
            'full_name': user.full_name,
            "intent": event,
            "error": error
        },
        'precision': 'ms'
    }
    try:
        await client.write(data)
    except InfluxDBWriteError as ex:
        logging.error(f'InfluxDB write error: {ex}')

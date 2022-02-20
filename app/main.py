import logging

from aiogram import Bot, Dispatcher, Router
from aioinflux import InfluxDBClient

from app import handlers, middlewares
from app.config import Config
from app.utils import logger
from app.utils.db import MyBeanieMongo
from app.utils.db.mongo_storage import MongoStorage
from app.utils.notifications.startup_notify import notify_superusers
from app.utils.set_bot_commands import set_commands


async def main():
    bot = Bot(token=Config.BOT_TOKEN, parse_mode='HTML')
    storage = await MongoStorage.from_url(
        Config.MONGODB_URI,
        f"{Config.MONGODB_DATABASE}_fsm",
    )
    dp = Dispatcher(storage=storage)
    influx_client = InfluxDBClient(
        host=Config.INFLUX_HOST,
        db=Config.INFLUX_DB,
        username=Config.INFLUX_USER,
        password=Config.INFLUX_PASSWORD,
    )

    admin_router = Router()
    dp.include_router(admin_router)
    regular_router = Router()
    dp.include_router(regular_router)

    middlewares.setup(dp, influx_client)
    handlers.setup_all_handlers(regular_router, admin_router)
    logger.setup_logger()

    mongo = MyBeanieMongo()
    await mongo.init_db()

    await notify_superusers(bot)
    await set_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        logging.warning("Shutting down..")
        await bot.session.close()
        storage.close()
        await mongo.close()
        logging.warning("Bye!")

import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import start_polling
from motor.motor_asyncio import AsyncIOMotorClient

from app import handlers, middlewares, filters
from app.config import Config
from app.utils import logger
from app.utils.db import MyODManticMongo
from app.utils.notifications.startup_notify import notify_superusers
from app.utils.set_bot_commands import set_commands


async def on_startup(dp):
    middlewares.setup(dp)
    filters.setup(dp)
    handlers.setup_all_handlers(dp)
    logger.setup_logger()

    mongo = MyODManticMongo()

    dp.bot["mongo"]: AsyncIOMotorClient = mongo

    await notify_superusers(Config.ADMINS)
    await set_commands(dp)


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    if mongo := dp.bot.get('mongo', None):
        await mongo.close()
        await mongo.wait_closed()
    logging.warning("Bye!")


def main():
    bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MongoStorage(host=Config.MONGODB_HOSTNAME,
                           db_name=f"{Config.MONGODB_DATABASE}_fsm",
                           password=Config.MONGODB_PASSWORD,
                           uri=Config.MONGODB_URI)
    dp = Dispatcher(bot, storage=storage)

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

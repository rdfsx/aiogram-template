import logging

from aiogram import Bot, Dispatcher, Router

from app import handlers, middlewares
from app.config import Config
from app.utils import logger
from app.utils.broadcast import MemoryBroadcastBotLocker
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

    admin_router = Router()
    dp.include_router(admin_router)
    regular_router = Router()
    dp.include_router(regular_router)

    middlewares.setup(dp)
    handlers.setup_all_handlers(regular_router, admin_router)
    logger.setup_logger()

    mongo = MyBeanieMongo()
    await mongo.init_db()

    await notify_superusers(bot)
    await set_commands(bot)

    broadcast_locker = MemoryBroadcastBotLocker()

    try:
        await dp.start_polling(bot, broadcast_locker=broadcast_locker)
    finally:
        logging.warning("Shutting down..")
        await bot.session.close()
        storage.close()
        await mongo.close()
        logging.warning("Bye!")

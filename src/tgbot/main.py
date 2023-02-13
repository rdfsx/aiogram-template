import asyncio
import logging
import signal

from aiogram import Bot, Dispatcher, Router

from src.tgbot import handlers, middlewares
from src.tgbot.config import Config
from src.tgbot.utils import logger
from src.tgbot.utils.db import MyBeanieMongo
from src.tgbot.utils.db.mongo_storage import MongoStorage
from src.tgbot.utils.set_bot_commands import set_commands
from src.tgbot.utils.startup_notify import notify_superusers


async def main():
    bot = Bot(token=Config.BOT_TOKEN, parse_mode="HTML")
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

    try:
        await dp.start_polling(bot)
    finally:
        logging.warning("Shutting down..")
        await bot.session.close()
        storage.close()
        await mongo.close()
        logging.warning("Bye!")


def handle_sigterm(*_):
    raise KeyboardInterrupt()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Goodbye")

from aiogram import Bot

from src.tgbot.config import Config
from src.tgbot.utils.broadcasting import broadcast, from_iterable


async def notify_superusers(bot: Bot) -> int:
    admins = Config.ADMINS
    for admin in admins:
        await bot.send_message(admin, "The bot is running!")

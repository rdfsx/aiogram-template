from aiogram import Bot

from src.tgbot.config import Config
from src.tgbot.utils.broadcasting import broadcast, from_iterable


async def notify_superusers(bot: Bot) -> int:
    admins = from_iterable(Config.ADMINS)
    return await broadcast(admins, bot.send_message, False, text="The bot is running!")

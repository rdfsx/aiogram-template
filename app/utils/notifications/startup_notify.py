from aiogram import Bot

from app.config import Config
from app.utils.broadcast import broadcast_smth, from_iterable


async def notify_superusers(bot: Bot) -> int:
    admins = from_iterable(Config.ADMINS)
    return await broadcast_smth(admins, bot.send_message, False, text='The bot is running!')

from aiogram import types
from aiogram.types import BotCommandScopeChat

from app.config import Config


async def set_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
        ]
    )
    for admin in Config.ADMINS:
        await dp.bot.set_my_commands(
            [
                types.BotCommand("amount", "Количество юзеров в бд"),
                types.BotCommand("exists_amount", "Количество живых юзеров"),
                types.BotCommand("broadcast", "Рассылка по всем юзерам"),
                types.BotCommand("users_file", 'Записать юзеров в файл')
            ],
            BotCommandScopeChat(admin)
        )

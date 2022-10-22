from aiogram import Bot, types
from aiogram.types import BotCommandScopeChat

from src.tgbot.config import Config


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(command="help", description="Вывести справку"),
        ]
    )
    for admin in Config.ADMINS:
        await bot.set_my_commands(
            [
                types.BotCommand(command="amount", description="Количество юзеров в бд"),
                types.BotCommand(command="chat_amount", description="Количество групп в бд"),
                types.BotCommand(
                    command="chat_users_amount",
                    description="Количество пользователей во всех группах",
                ),
                types.BotCommand(command="exists_amount", description="Количество живых юзеров"),
                types.BotCommand(command="broadcast", description="Рассылка по всем юзерам"),
                types.BotCommand(command="users_file", description="Записать юзеров в файл"),
            ],
            BotCommandScopeChat(chat_id=admin),
        )

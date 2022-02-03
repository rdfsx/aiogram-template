import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Union

from aiofile import async_open
from aiogram import Bot, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, InputFile, CallbackQuery

from app.models import UserModel, ChatModel


async def get_amount_users(msg: Message, bot: Bot):
    await bot.send_chat_action(msg.chat.id, "typing")
    active_amount = await UserModel.find(UserModel.status == "member").count()
    left_amount = await UserModel.find(UserModel.status == "left").count()
    amount = await UserModel.find_all().count()
    now = datetime.now()
    last_day_amount = await UserModel.find(UserModel.created_at > (now - timedelta(days=1))).count()
    last_week_amount = await UserModel.find(UserModel.created_at > (now - timedelta(weeks=1))).count()
    last_month_amount = await UserModel.find(UserModel.created_at > (now - timedelta(days=31))).count()
    await msg.answer(
        "\n".join(
            [
                f"Участники (включая удалённые аккаунты): {active_amount}",
                f"За последние сутки: {last_day_amount}",
                f"За последнюю неделю: {last_week_amount}",
                f"За последний месяц: {last_month_amount}",
                f"Выключенные: {left_amount}",
                f"Всего в бд: {amount}",
            ]
        )
    )


async def get_amount_chats(msg: Message):
    amount = await ChatModel.find(ChatModel.type != "private").count()
    await msg.answer(f"Количество групп в базе данных: {amount}")


async def get_amount_chats_users(msg: Message, bot: Bot):
    await msg.answer("Начинаем подсчет...")
    amount = 0
    for group in await ChatModel.find(ChatModel.type != "private").to_list():
        try:
            amount += await bot.get_chat_member_count(group.id)
        except Exception as e:
            logging.error(e)
            await group.delete()
    await msg.answer(f"Количество пользователей в группах: {amount}")


async def get_exists_users(m: Message, bot: Bot):
    await m.answer("Начинаем подсчет...")
    users = await UserModel.find_all().to_list()
    count = 0
    for user in users:
        try:
            if await bot.send_chat_action(user.id, "typing"):
                user.status = "member"
                await user.save()
                count += 1
        except TelegramAPIError:  # TODO check if it working
            await user.delete()
        except Exception as e:
            user.status = "left"
            await user.save()
            logging.exception(e)
        await asyncio.sleep(.05)
    await m.answer(f"Активных пользователей: {count}")


async def write_users_to_file(m: Message):
    await m.answer("Начинаем запись...")
    users = await UserModel.find_all().to_list()
    filename = 'users.txt'
    async with async_open(filename, mode='w') as f:
        for user in users:
            await f.write(f"{user.id}\n")
    await m.answer_document(InputFile(filename))
    os.remove(filename)


async def cancel_all(ctx: Union[CallbackQuery, Message], state: FSMContext):
    await state.clear()
    msg = ctx
    if isinstance(ctx, CallbackQuery):
        await ctx.answer()
        msg = ctx.message
        await msg.delete()
    await msg.answer('Отменено.')


def setup(router: Router):
    router.message.register(get_amount_users, commands="amount")
    router.message.register(get_amount_chats, commands="chat_amount")
    router.message.register(get_amount_chats_users, commands="chat_users_amount")
    router.message.register(get_exists_users, commands="exists_amount")
    router.message.register(write_users_to_file, commands="users_file")
    router.callback_query.register(cancel_all, text='cancel', state='*')
    router.message.register(cancel_all, commands="/cancel", state='*')

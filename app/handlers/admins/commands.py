import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Union

from aiofile import async_open
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery
from aiogram.utils.exceptions import UserDeactivated

from app.models import UserModel, ChatModel


async def get_amount_users(m: Message):
    await m.answer_chat_action("typing")
    active_amount = await UserModel.find(UserModel.status == "member").count()
    left_amount = await UserModel.find(UserModel.status == "left").count()
    amount = await UserModel.find_all().count()
    now = datetime.now()
    last_day_amount = await UserModel.find(UserModel.created_at > (now - timedelta(days=1))).count()
    last_week_amount = await UserModel.find(UserModel.created_at > (now - timedelta(weeks=1))).count()
    last_month_amount = await UserModel.find(UserModel.created_at > (now - timedelta(days=31))).count()
    await m.answer(
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


async def get_amount_chats(m: Message):
    amount = await ChatModel.find(ChatModel.type != "private").count()
    await m.answer(f"Количество групп в базе данных: {amount}")


async def get_amount_chats_users(m: Message):
    await m.answer("Начинаем подсчет...")
    amount = 0
    for group in await ChatModel.find(ChatModel.type != "private").to_list():
        try:
            amount += await m.bot.get_chat_member_count(group.id)
        except Exception as e:
            logging.error(e)
            await group.delete()
    await m.answer(f"Количество пользователей в группах: {amount}")


async def get_exists_users(m: Message):
    await m.answer("Начинаем подсчет...")
    bot = m.bot
    users = await UserModel.find_all().to_list()
    count = 0
    for user in users:
        try:
            if await bot.send_chat_action(user.id, "typing"):
                user.status = "member"
                await user.save()
                count += 1
        except UserDeactivated:
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
    await state.reset_state()
    msg = ctx
    if isinstance(ctx, CallbackQuery):
        await ctx.answer()
        msg = ctx.message
        await msg.delete()
    await msg.answer('Отменено.')


def setup(dp: Dispatcher):
    dp.register_message_handler(get_amount_users, commands="amount", is_admin=True)
    dp.register_message_handler(get_amount_chats, commands="chat_amount", is_admin=True)
    dp.register_message_handler(get_amount_chats_users, commands="chat_users_amount", is_admin=True)
    dp.register_message_handler(get_exists_users, commands="exists_amount", is_admin=True)
    dp.register_message_handler(write_users_to_file, commands="users_file", is_admin=True)
    dp.register_callback_query_handler(cancel_all, text='cancel', state='*', is_admin=True)
    dp.register_message_handler(cancel_all, commands="/cancel", state='*', is_admin=True)

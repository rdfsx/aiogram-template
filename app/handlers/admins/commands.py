import asyncio
import logging
import os
from typing import Union

from aiofile import async_open
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery
from aiogram.utils.exceptions import UserDeactivated
from odmantic import AIOEngine

from app.models import UserModel, ChatModel


async def get_amount_users(m: Message, db: AIOEngine):
    await m.answer_chat_action("typing")
    active_amount = await db.count(UserModel, UserModel.status == "member")
    left_amount = await db.count(UserModel, UserModel.status == "left")
    amount = await db.count(UserModel)
    await m.answer(
        "\n".join(
            [
                f"Участники (включая удалённые аккаунты): {active_amount}",
                f"Выключенные: {left_amount}",
                f"Итого: {amount}",
            ]
        )
    )


async def get_amount_chats(m: Message, db: AIOEngine):
    amount = await db.count(ChatModel, ChatModel.type != "private")
    await m.answer(f"Количество групп в базе данных: {amount}")


async def get_amount_chats_users(m: Message, db: AIOEngine):
    await m.answer("Начинаем подсчет...")
    amount = 0
    for group in await db.find(ChatModel, ChatModel.type != "private"):
        try:
            amount += await m.bot.get_chat_member_count(group.id)
        except Exception as e:
            logging.error(e)
            await db.delete(group)
    await m.answer(f"Количество пользователей в группах: {amount}")


async def get_exists_users(m: Message, db: AIOEngine):
    await m.answer("Начинаем подсчет...")
    bot = m.bot
    users = await db.find(UserModel)
    count = 0
    for user in users:
        try:
            if await bot.send_chat_action(user.id, "typing"):
                count += 1
        except UserDeactivated:
            await db.delete(user)
        except Exception as e:
            user.status = "left"
            await db.save(user)
            logging.exception(e)
        await asyncio.sleep(.05)
    await m.answer(f"Активных пользователей: {count}")


async def write_users_to_file(m: Message, db: AIOEngine):
    await m.answer("Начинаем запись...")
    users = await db.find(UserModel)
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

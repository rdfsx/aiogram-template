import asyncio
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.exceptions import RetryAfter

from app.keyboards.admin.inline import CancelKb
from app.models import UserModel
from app.states.admin_states import BroadcastAdmin


async def start_broadcast(m: Message):
    await BroadcastAdmin.BROADCAST.set()
    await m.answer('Введите сообщение, которое хотели бы отправить всем, кто есть в базе:',
                   reply_markup=CancelKb().get())


async def start_broadcasting(m: Message, state: FSMContext):
    await m.answer("Рассылка запущена.")
    await state.reset_state()
    chats = UserModel.find()
    i = 0
    async for chat in chats:
        try:
            await m.send_copy(chat.id)
            i += 1
        except RetryAfter as e:
            logging.error(f"Target [ID:{chat.id}]: Flood limit is exceeded. "
                          f"Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
        except Exception as e:
            logging.error(e)
        await asyncio.sleep(0.05)
    await m.answer(f"Отправлено {i} сообщений.")


def setup(dp: Dispatcher):
    dp.register_message_handler(start_broadcast, commands="broadcast", is_admin=True)
    dp.register_message_handler(start_broadcasting, state=BroadcastAdmin.BROADCAST, is_admin=True,
                                content_types=types.ContentType.ANY)




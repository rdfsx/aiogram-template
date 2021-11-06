from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_broadcaster import MessageBroadcaster
from odmantic import AIOEngine

from app.keyboards.inline import CancelMarkup
from app.models import UserModel
from app.states.admin_states import BroadcastAdmin


async def start_broadcast(m: Message):
    await BroadcastAdmin.BROADCAST.set()
    await m.answer('Введите сообщение, которое хотели бы отправить всем, кто есть в базе:',
                   reply_markup=CancelMarkup().get())


async def cancel_broadcast(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.answer()
    await call.message.answer('Отменено.')


async def start_broadcasting(m: Message, state: FSMContext, db: AIOEngine):
    chats = await db.find(UserModel)
    broadcaster = MessageBroadcaster(chats=[chat.id for chat in chats], message=m)
    await state.reset_state()
    await m.answer("Рассылка запущена.")
    await broadcaster.run()
    await m.answer(f"Отправлено {len(broadcaster._successful)} сообщений.")


def setup(dp: Dispatcher):
    dp.register_message_handler(start_broadcast, commands="broadcast", is_admin=True)
    dp.register_callback_query_handler(cancel_broadcast, text='cancel', state='*', is_admin=True)
    dp.register_message_handler(start_broadcasting, state=BroadcastAdmin.BROADCAST, is_admin=True,
                                content_types=types.ContentType.ANY)




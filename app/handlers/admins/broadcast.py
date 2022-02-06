from aiogram import types, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.admin.inline import CancelKb
from app.models import UserModel
from app.states.admin_states import BroadcastAdmin
from app.utils.broadcast import broadcast_smth


async def start_broadcast(msg: Message, state: FSMContext):
    await state.set_state(BroadcastAdmin.BROADCAST)
    await msg.answer('Введите сообщение, которое хотели бы отправить всем, кто есть в базе:',
                     reply_markup=CancelKb().get())


async def start_broadcasting(msg: Message, state: FSMContext):
    info_msg = await msg.answer("Рассылка запущена.")
    await state.clear()

    chats = UserModel.find()

    async def send_copy(chat_id: int, count: int, message: Message, red_msg: Message) -> int:
        await message.send_copy(chat_id)
        count += 1
        if count % 10 == 0:
            await red_msg.edit_text(f"Отправлено {count} сообщений.")
        return count

    amount = await broadcast_smth(chats, send_copy, True, 'id', message=msg, red_msg=info_msg)

    await info_msg.edit_text(f"Рассылка завершена. Отправлено {amount} сообщений.")


def setup(router: Router):
    router.message.register(start_broadcast, commands="broadcast")
    router.message.register(start_broadcasting, state=BroadcastAdmin.BROADCAST, content_types=types.ContentType.ANY)

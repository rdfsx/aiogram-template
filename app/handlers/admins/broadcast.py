from typing import cast, AsyncGenerator

from aiogram import types, Router, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.admin.reply import CancelMarkup
from app.models import UserModel
from app.states.admin_states import BroadcastAdmin
from app.utils.broadcast import broadcast_smth, MemoryBroadcastBotLocker
from app.utils.exceptions import BroadcastLockException


async def start_broadcast(msg: Message, state: FSMContext, broadcast_locker: MemoryBroadcastBotLocker, bot: Bot):
    if broadcast_locker.is_exist(bot.id):
        return msg.answer("Рассылка уже была запущена ранее. Дождитесь завершения рассылки, чтобы начать новую.")
    await state.set_state(BroadcastAdmin.BROADCAST)
    await msg.answer('Введите сообщение, которое хотели бы отправить всем, кто есть в базе:',
                     reply_markup=CancelMarkup().get())


async def cancel_broadcast(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Отменено.", reply_markup=ReplyKeyboardRemove())


async def start_broadcasting(msg: Message, state: FSMContext, broadcast_locker: MemoryBroadcastBotLocker, bot: Bot):
    await msg.answer("OK", reply_markup=ReplyKeyboardRemove())
    info_msg = await msg.answer("Рассылка запущена.")
    await state.clear()

    chats = UserModel.find()

    async def send_copy(chat_id: int, count: int, message: Message, red_msg: Message) -> int:
        try:
            await message.send_copy(chat_id)

        except Exception as e:
            user = await UserModel.find_one(UserModel.id == chat_id)
            user.status = "left"
            await user.save()
            raise e

        count += 1
        if count % 10 == 0:
            await red_msg.edit_text(f"Отправлено {count} сообщений.")
        return count

    try:
        async with broadcast_locker.lock(bot.id):
            amount = await broadcast_smth(
                cast(AsyncGenerator, chats), send_copy, True, 'id', message=msg, red_msg=info_msg
            )
            await info_msg.edit_text(f"Рассылка завершена. Отправлено {amount} сообщений.")

    except BroadcastLockException:
        await info_msg.edit_text("Рассылка уже была запущена ранее. "
                                 "Дождитесь завершения рассылки, чтобы начать новую.")


def setup(router: Router):
    router.message.register(start_broadcast, commands="broadcast")
    router.message.register(cancel_broadcast, text="Отмена", state=BroadcastAdmin.BROADCAST)
    router.message.register(start_broadcasting, state=BroadcastAdmin.BROADCAST, content_types=types.ContentType.ANY)

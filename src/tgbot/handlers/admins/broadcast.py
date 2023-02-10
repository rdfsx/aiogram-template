from typing import AsyncGenerator, cast

from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from src.tgbot.keyboards.reply import cancel_markup
from src.tgbot.models import UserModel
from src.tgbot.utils.broadcasting import broadcast, send_copy
from src.tgbot.utils.exceptions import BroadcastLockException
from src.tgbot.utils.states.admin_states import BroadcastAdmin


async def start_broadcast(
    msg: Message,
    state: FSMContext,
):
    await state.set_state(BroadcastAdmin.BROADCAST)
    await msg.answer(
        "Введите сообщение, которое хотели бы отправить всем, кто есть в базе:",
        reply_markup=cancel_markup,
    )


async def cancel_broadcast(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Отменено.", reply_markup=ReplyKeyboardRemove())


async def start_broadcasting(
    msg: Message,
    state: FSMContext,
):
    await msg.answer("OK", reply_markup=ReplyKeyboardRemove())
    info_msg = await msg.answer("Рассылка запущена.")
    await state.clear()

    try:
        amount = await broadcast(
            cast(AsyncGenerator, UserModel.safe_find()),
            send_copy,
            True,
            "id",
            message=msg,
            red_msg=info_msg,
        )
        await info_msg.edit_text(f"Рассылка завершена. Отправлено {amount} сообщений.")

    except BroadcastLockException:
        await info_msg.edit_text(
            "Рассылка уже была запущена ранее. "
            "Дождитесь завершения рассылки, чтобы начать новую."
        )


def setup(router: Router):
    router.message.register(start_broadcast, Command("broadcast"))
    router.message.register(cancel_broadcast, Text("Отмена"), State(BroadcastAdmin.BROADCAST))
    router.message.register(
        start_broadcasting,
        State(BroadcastAdmin.BROADCAST),
        F.content_type.in_({types.ContentType.ANY}),
    )

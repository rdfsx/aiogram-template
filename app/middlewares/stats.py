from asyncio import create_task

from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.utils.chatbase import ChatbaseMessage


class StatsMiddleware(BaseMiddleware):

    @staticmethod
    async def setup_stats(user_id: int, message: str = '', intent: str = ''):
        handler = current_handler.get()
        if not handler:
            return
        handler_name = handler.__name__
        msg = ChatbaseMessage(
            user_id=str(user_id),
            message=message,
            intent=intent or handler_name
        )
        create_task(msg.send())

    async def on_process_message(self, m: types.Message, *args, **kwargs):
        await self.setup_stats(m.from_user.id, m.text)

    async def on_process_callback_query(self, q: types.CallbackQuery, *args, **kwargs):
        await self.setup_stats(q.from_user.id, q.data)

    async def on_process_inline_query(self, iq: types.InlineQuery, *args, **kwargs):
        await self.setup_stats(iq.from_user.id, iq.query)

    async def on_pre_process_chosen_inline_result(self, ciq: types.ChosenInlineResult, *args, **kwargs):
        await self.setup_stats(ciq.from_user.id, ciq.query, 'process_inline_result')

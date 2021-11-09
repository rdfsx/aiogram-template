from aiogram import types, Bot
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware


class ClocksMiddleware(BaseMiddleware):

    @staticmethod
    async def setup_chat(data: dict, chat: types.Chat):
        handler = current_handler.get()
        allow = hasattr(handler, "clocks")
        if not allow:
            return
        chat_id = int(chat.id)
        bot = Bot.get_current()
        msg = await bot.send_message(chat_id, "⏳")
        await bot.send_chat_action(chat_id, "typing")

        data["clocks_msg"]: types.Message = msg

    @staticmethod
    async def close_chat(data: dict):
        if msg := data.get('clocks_msg', None):
            await msg.delete()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.chat)

    async def on_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.message.chat if query.message else None)

    async def on_post_process_message(self, message: types.Message, args: list, data: dict):
        await self.close_chat(data)

    async def on_post_process_callback_query(self, query: types.CallbackQuery, args: list, data: dict):
        await self.close_chat(data)

from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models import ChatModel, UserModel
from app.utils.notifications.new_notify import notify_new_user, notify_new_group


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(data: dict, user: types.User, language: str, chat: Optional[types.Chat] = None):
        user_id = int(user.id)
        chat_id = int(chat.id)
        chat_type = chat.type if chat else "private"

        if not (user_db := await UserModel.find_one(UserModel.id == user_id)):
            user_db = await UserModel(id=user_id, language=language).create()
            await notify_new_user(user)
        if not (chat_db := await ChatModel.find_one(ChatModel.id == chat_id)):
            chat_db = await ChatModel(id=chat_id, type=chat_type).create()
            if chat_type != types.ChatType.PRIVATE:
                await notify_new_group(chat)

        data["user"]: UserModel = user_db
        data["chat"]: ChatModel = chat_db

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message.from_user.language_code, message.chat)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user, query.from_user.language_code,
                              query.message.chat if query.message else None)

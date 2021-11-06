from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from odmantic import AIOEngine

from app.models import ChatModel, UserModel
from app.utils.db import MyODManticMongo
from app.utils.notifications.new_notify import notify_new_user


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(data: dict, user: types.User, language: str, chat: Optional[types.Chat] = None):
        user_id = int(user.id)
        chat_id = int(chat.id)
        chat_type = chat.type if chat else "private"
        mongo: MyODManticMongo = chat.bot["mongo"]
        db: AIOEngine = mongo.get_engine()

        if not (user_db := await db.find_one(UserModel, UserModel.id == user_id)):
            user_db = await db.save(UserModel(id=user_id, language=language))
            await notify_new_user(user)
        if not (chat_db := await db.find_one(ChatModel, ChatModel.id == chat_id)):
            chat_db = await db.save(ChatModel(id=chat_id, type=chat_type))

        data["user"]: UserModel = user_db
        data["chat"]: ChatModel = chat_db

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message.from_user.language_code, message.chat)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user, query.from_user.language_code,
                              query.message.chat if query.message else None)

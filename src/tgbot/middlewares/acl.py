from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User

from src.tgbot.models import ChatModel, UserModel


class ACLMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user")
        chat: Optional[Chat] = data.get("event_chat")

        if user:
            if not (user_db := await UserModel.find_one(UserModel.id == user.id)):
                user_db = UserModel(id=user.id, language_code=user.language_code)

                if chat and chat.type == "private":
                    await user_db.create()

            data["user"] = user_db

        if chat:
            if not (chat_db := await ChatModel.find_one(ChatModel.id == chat.id)):
                chat_db = await ChatModel(id=chat.id, type=chat.type).create()

            data["chat"] = chat_db

        return await handler(event, data)

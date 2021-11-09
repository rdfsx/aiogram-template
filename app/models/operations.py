from typing import Type, Any

from aiogram import Bot
from odmantic import AIOEngine, Model


class ChatCommands:
    def __init__(self, db: AIOEngine = None):
        if not db:
            self.db: AIOEngine = Bot.get_current()["db"]
        else:
            self.db: AIOEngine = db

    async def get(self, _id: Any, model: Type[Model]):
        return await self.db.find_one(model, model.id == _id)

    async def get_all(self, model: Type[Model]) -> list:
        return await self.db.find(model)

    async def put(self, _id: Any, model: Type[Model], **kwargs):
        if not (instance := await self.db.find_one(model, model.id == _id)):
            instance = model(id=_id, **kwargs)
            await self.db.save(instance)
        else:
            for prop, value in kwargs.items():
                instance.__setattr__(prop, value)
            await self.db.save(instance)
        return instance

    async def delete(self, _id: Any, model: Type[Model]) -> bool:
        instance = await self.db.find_one(model, model.id == _id)
        if instance is not None:
            await self.db.delete(instance)
            return True
        return False

    async def post(self, _id: Any, model: Type[Model], **kwargs):
        if not (instance := await self.db.find_one(model, model.id == _id)):
            instance = await self.db.save(model(id=_id, **kwargs))
        return instance

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from odmantic import AIOEngine

from app.utils.db import MyODManticMongo


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['update']

    def __init__(self):
        super(DatabaseMiddleware, self).__init__()

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        mongo: MyODManticMongo = obj.bot["mongo"]
        db = mongo.get_engine()
        data["db"]: AIOEngine = db

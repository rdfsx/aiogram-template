import logging
from typing import Optional

import pymongo.errors
from motor.core import AgnosticDatabase, AgnosticCollection, AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from odmantic import AIOEngine

from app.config import Config
from app.utils.db.my_engine import MyAIOEngine


class MyMongoClient:
    def __init__(self, db_name=Config.MONGODB_DATABASE, uri=Config.MONGODB_URI):
        self._db_name: str = db_name
        self._uri = uri

        self._mongo: Optional[AgnosticClient] = None
        self._db: Optional[AgnosticDatabase] = None

    def get_client(self) -> AgnosticClient:
        if isinstance(self._mongo, AsyncIOMotorClient):
            return self._mongo
        try:
            logging.debug("Connection to {}", self._uri)
            self._mongo = AsyncIOMotorClient(self._uri)
            logging.debug("Connected successful")
        except pymongo.errors.ConfigurationError as e:
            if "query() got an unexpected keyword argument 'lifetime'" in e.args[0]:
                logging.warning(
                    "Run `pip install dnspython==1.16.0` in order to fix ConfigurationError. "
                    "More information: https://github.com/mongodb/mongo-python-driver/pull/423#issuecomment-528998245")
            raise e
        return self._mongo

    def get_db(self) -> AgnosticDatabase:
        if isinstance(self._db, AsyncIOMotorDatabase):
            return self._db

        client = self.get_client()
        self._db = client.get_database(self._db_name)

        return self._db

    async def get_coll(self, collection_name: str) -> AgnosticCollection:
        return self.get_db()[collection_name]

    async def close(self):
        if self._mongo:
            self._mongo.close()

    @staticmethod
    async def wait_closed():
        return True


class MyODManticMongo(MyMongoClient):

    _engine: Optional[AIOEngine] = None

    def get_engine(self) -> AIOEngine:
        if not self._engine:
            self._engine = MyAIOEngine(motor_client=self.get_client(), database=Config.MONGODB_DATABASE)
        return self._engine

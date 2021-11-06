from aiogram import Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .acl import ACLMiddleware
from .database import DatabaseMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(EnvironmentMiddleware())
    dp.setup_middleware(DatabaseMiddleware())
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(ThrottlingMiddleware())

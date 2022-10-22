from aiogram import Dispatcher

from .acl import ACLMiddleware
from .clocks import ClocksMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(ClocksMiddleware())
    dp.callback_query.middleware(ClocksMiddleware())
    dp.update.outer_middleware(ACLMiddleware())

from aiogram import Dispatcher

from app.handlers.errors import catcher


def setup(dp: Dispatcher):
    for module in (catcher, ):
        module.setup(dp)

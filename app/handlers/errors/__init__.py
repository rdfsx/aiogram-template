from aiogram import Dispatcher

from app.handlers.errors import error_handler


def setup(dp: Dispatcher):
    for module in (error_handler, ):
        module.setup(dp)

from aiogram import Dispatcher

from app.handlers.updates import status


def setup(dp: Dispatcher):
    for module in (status, ):
        module.setup(dp)

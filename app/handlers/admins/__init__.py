from aiogram import Dispatcher

from app.handlers.admins import broadcast, commands


def setup(dp: Dispatcher):
    for module in (broadcast, commands):
        module.setup(dp)

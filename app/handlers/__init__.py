from aiogram import Dispatcher

from app.handlers import admins, private, errors


def setup_all_handlers(dp: Dispatcher):
    for module in (admins, private, errors):
        module.setup(dp)

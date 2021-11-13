from aiogram import Dispatcher

from app.handlers import admins, private, errors
from app.handlers.updates import status


def setup_all_handlers(dp: Dispatcher):
    for module in (admins, private, errors, status):
        module.setup(dp)

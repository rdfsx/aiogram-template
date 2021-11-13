from aiogram import Dispatcher

from app.handlers import admins, private, errors
from app.handlers import updates


def setup_all_handlers(dp: Dispatcher):
    for module in (admins, private, errors, updates):
        module.setup(dp)

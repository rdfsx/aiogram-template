from aiogram import Router

from src.tgbot.handlers.errors import catcher


def setup(router: Router):
    for module in (catcher,):
        module.setup(router)

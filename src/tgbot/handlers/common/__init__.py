from aiogram import Router

from src.tgbot.handlers.common import default, start, status


def setup(router: Router):
    for module in (start, default, status):
        module.setup(router)

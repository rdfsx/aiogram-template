from aiogram import Router

from src.tgbot.filters.admin import AdminFilter
from src.tgbot.handlers.admins import broadcast, commands


def setup(router: Router):
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminFilter())

    for module in (broadcast, commands):
        module.setup(router)

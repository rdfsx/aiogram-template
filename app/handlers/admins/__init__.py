from aiogram import Router

from app.filters.admin import AdminFilter
from app.handlers.admins import broadcast, commands


def setup(router: Router):
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminFilter())

    for module in (broadcast, commands):
        module.setup(router)

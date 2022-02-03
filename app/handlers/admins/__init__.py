from aiogram import Dispatcher, Router

from app.filters.is_admin import AdminFilter
from app.handlers.admins import broadcast, commands


def setup(dp: Dispatcher):
    router = Router()

    router.message.bind_filter(AdminFilter)
    router.callback_query.bind_filter(AdminFilter)

    dp.include_router(router)

    for module in (broadcast, commands):
        module.setup(dp)

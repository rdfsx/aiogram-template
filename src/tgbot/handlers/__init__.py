from aiogram import Router

from src.tgbot.handlers import admins, common, errors


def setup_all_handlers(router: Router, admin_router: Router):
    admins.setup(admin_router)

    for module in (common, errors):
        module.setup(router)

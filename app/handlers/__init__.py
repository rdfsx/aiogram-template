from aiogram import Dispatcher, Router

from app.handlers import admins, private, errors
from app.handlers import updates


def setup_all_handlers(router: Router, admin_router: Router):
    admins.setup(admin_router)

    for module in (private, errors, updates):
        module.setup(router)

import logging

from aiogram import Router
from aiogram.types import Message, Update
from aiogram.utils.markdown import hcode

logger = logging.getLogger(__name__)


async def errors_handler(update: Update, exception):
    text = "Вызвано необрабатываемое исключение. Перешлите это сообщение администратору.\n"
    error = f"Error: {type(exception)}: {exception}\n\nUpdate: {update}"
    logger.exception(error)
    msg = update if isinstance(update, Message) else update.message
    await msg.answer(f"{text}{hcode(error)}")


def setup(router: Router):
    router.errors.register(errors_handler)

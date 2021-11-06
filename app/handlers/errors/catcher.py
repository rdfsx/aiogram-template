import logging

from aiogram import Dispatcher
from aiogram.types import Update, Message
from aiogram.utils.markdown import hcode


async def errors_handler(update: Update, exception):
    text = "Вызвано необрабатываемое исключение. Перешлите это сообщение администратору.\n"
    error = f'Error: {type(exception)}: {exception}\n\nUpdate: {update}'
    logging.exception(error)
    msg = update if isinstance(update, Message) else update.message
    await msg.answer(f"{text}{hcode(error)}")


def setup(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)

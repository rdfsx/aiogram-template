import logging

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.markdown import hcode


async def errors_handler(update, exception):
    text = "Вызвано необрабатываемое исключение. Перешлите это сообщение администратору.\n"
    error = f'Error: {exception}\nUpdate: {update}'
    logging.exception(error)
    await Update.get_current().message.answer(text + hcode(error))


def setup(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)

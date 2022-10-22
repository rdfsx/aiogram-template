from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_builder = ReplyKeyboardBuilder()

cancel_markup = reply_builder.row(
    KeyboardButton(
        text="Cancel",
    )
)

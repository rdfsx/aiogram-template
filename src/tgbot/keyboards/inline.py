from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_builder = InlineKeyboardBuilder()

cancel_kb = inline_builder.row(
    InlineKeyboardButton(
        text="Cancel",
        callback_data="cancel",
    )
)

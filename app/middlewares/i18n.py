from dataclasses import dataclass, field
from functools import partial
from pathlib import Path

import i18n
from aiogram import types, Bot
from aiogram.dispatcher.middlewares import BaseMiddleware


@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseMiddleware):
    AVAILABLE_LANGUAGES = {
        "en": LanguageData("🇬🇧", "English"),
        "ru": LanguageData("🇷🇺", "Русский"),
    }

    def __init__(self, path: Path, default='en'):
        super(I18nMiddleware, self).__init__()

        self.default = default
        i18n.load_path.append(path)
        self.i18n = i18n

    async def get_user_locale(self, data: dict):
        language = self.default
        if "user" in data:
            language = data["user"].real_language or self.default
        data["i18n"] = partial(self.i18n.t, locale=language)

    async def on_pre_process_message(self, _: types.Message, data: dict):
        await self.get_user_locale(data)

    async def on_pre_process_callback_query(self, _: types.CallbackQuery, data: dict):
        await self.get_user_locale(data)

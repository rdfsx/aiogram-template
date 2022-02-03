from contextlib import suppress
from typing import Dict, List, Union

from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup

from .base import BaseMarkupConstructor


class ReplyMarkupConstructor(BaseMarkupConstructor):
    """
    Class for creating reply keyboards
    Usage example:
        class ExampleReplyMarkup(ReplyMarkupConstructor):
            def get(self):
                schema = [1, 2, 3, 3]
                actions = [
                    {'text': '1', },
                    {'text': '2', 'contact': True},
                    {'text': '3', 'location': True},
                    {'text': '4', 'poll': True},
                    {'text': '5', 'request_contact': True},
                    {'text': '6', 'request_location': True},
                    {'text': '7', 'request_poll': None},
                    {'text': '8', 'request_poll': "regular"},
                    {'text': '9', 'request_poll': KeyboardButtonPollType(type="regular")},
                ]
                return self.markup(actions, schema)
    """

    aliases = {
        "request_contact": "contact",
        "request_location": "location",
        "request_poll": "poll",
    }
    available_properties = ["text", "request_contact", "request_location", "request_poll"]
    properties_amount = 2

    def _replace_aliases(
        self,
        action: Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]],
    ):
        super()._replace_aliases(action)

    def _check_properties(
        self,
        action: Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]],
    ) -> Dict[str, Union[str, bool]]:
        return super()._check_properties(action)

    @staticmethod
    def _set_poll_property(button_data: dict) -> dict:
        with suppress(KeyError):
            if not isinstance(button_data["request_poll"], KeyboardButtonPollType):
                raise ValueError(
                    'Field "request_poll" must be of type KeyboardButtonPollType, str or None'
                )

        with suppress(KeyError):
            if isinstance(button_data["request_poll"], str) or button_data["request_poll"] is None:
                button_data["request_poll"] = KeyboardButtonPollType(
                    type=button_data["request_poll"]
                )
        return button_data

    def markup(
        self,
        actions: List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]],
        schema: List[int],
        resize_keyboard: bool = None,
        one_time_keyboard: bool = None,
        selective: bool = None,
    ) -> ReplyKeyboardMarkup:
        buttons = list()
        for action in actions:
            self._replace_aliases(action)
            button_data = self._set_poll_property(self._check_properties(action))
            buttons.append(KeyboardButton(**button_data))
        markup = ReplyKeyboardMarkup(
            keyboard=self.create_keyboard_layout(buttons, schema),
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
        )
        return markup

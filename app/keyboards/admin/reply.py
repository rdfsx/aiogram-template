from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup

from app.utils.markup_constructor import ReplyMarkupConstructor


class ExampleReplyMarkup(ReplyMarkupConstructor):
    def get(self) -> ReplyKeyboardMarkup:
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


class CancelMarkup(ReplyMarkupConstructor):
    def get(self) -> ReplyKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': 'Отмена'},
        ]
        return self.markup(actions, schema, True)

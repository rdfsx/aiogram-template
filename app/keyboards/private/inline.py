from aiogram.dispatcher.filters.callback_data import CallbackData

from app.utils.markup_constructor import InlineMarkupConstructor


class ExampleMarkup(InlineMarkupConstructor):
    class CD(CallbackData, prefix='test'):
        number: str

    def get(self):
        schema = [3, 2]
        actions = [
            {'text': '1', 'callback_data': self.CD(number='1')},
            {'text': '2', 'callback_data': self.CD(number='2').pack()},
            {'text': '3', 'callback_data': '3'},
            {'text': '4', 'callback_data': self.CD(number='4').pack()},
            {'text': '6', 'callback_data': '6'},
        ]
        return self.markup(actions, schema)

from aiogram.dispatcher.filters.state import StatesGroup, State


class AnswerAdmin(StatesGroup):
    ANSWER = State()


class BroadcastAdmin(StatesGroup):
    BROADCAST = State()

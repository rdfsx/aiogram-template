from aiogram.fsm.state import State, StatesGroup


class AnswerAdmin(StatesGroup):
    ANSWER = State()


class BroadcastAdmin(StatesGroup):
    BROADCAST = State()

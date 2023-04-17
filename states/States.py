from aiogram.dispatcher.filters.state import State, StatesGroup

class StateMessage(StatesGroup):
    translation = State()
    nickname = State()
    userid = State()
    description = State()
    end = State()
from aiogram.dispatcher.filters.state import State, StatesGroup

class StateMessage(StatesGroup):
    translation = State()
    nickname = State()
    description = State()
    end = State()
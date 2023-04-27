from aiogram.dispatcher.filters.state import State, StatesGroup

class StateMessage(StatesGroup):
    translation = State()
    nickname = State()
    userid = State()
    description = State()
    end = State()
    
class Payment(StatesGroup):
    currency = State()
    network = State()
    amount = State()
    end = State()

class PaymentСonclusion(StatesGroup):
    currency = State()
    network = State()
    address = State()
    amount = State()
    end = State()

class AddNewGame(StatesGroup):
    photo = State()
    namegame = State()
    cengame = State()
    loginaccount = State()
    password = State()
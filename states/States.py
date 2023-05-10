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
    amount = State()
    currency = State()
    network = State()
    address = State()
    end = State()

class AddNewGame(StatesGroup):
    sectionid = State()
    photo = State()
    namegame = State()
    cengame = State()
    loginaccount = State()
    password = State()

class Menu(StatesGroup):
    step = State()

class AddBalanceUsers(StatesGroup):
    login = State()
    depositAmount = State()
    end = State()

class Addsections(StatesGroup):
    name = State()

class Estimation(StatesGroup):
    estimation = State()
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from core.database import DataBase
from config import *

bot = Bot(
    token=TOKEN_TG, 
    parse_mode=types.ParseMode.HTML
)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase()
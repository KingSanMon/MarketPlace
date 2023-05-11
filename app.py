from aiogram import executor
from core.console import console
from loader import dp
from handlers.admin import *
from handlers.users import *
from filters.filters import *

from commands.set_bot_commands import set_default_commands
from middleware.middleware import UserUpdateLogin
from middleware.middleware import UserBanned

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    dp.middleware.setup(UserBanned())
    dp.middleware.setup(UserUpdateLogin())

if __name__ == '__main__':
    try:
        console.log("Бот запущен")
        executor.start_polling(dp, on_startup=on_startup)
    except Exception as err:
        logging.exception(err)


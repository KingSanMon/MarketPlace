from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import *
from states.States import *

# @dp.message_handler(commands=["start"], state="*", chat_type=["private"])
# async def start(message: types.Message, state: FSMContext):

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        f"Приветствуем вас в нашем <b>маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )
#  при кнопке старт заносим пользователя
    user = message.chat.username
    user_id = message.from_user.id
    date = message.date.strftime('%Y-%m-%d')
#  проверка есть ли пользователь в бд
    if db.get("SELECT id FROM users WHERE user_id = ?", (user_id,)) == None:
#  если нету регистрируем его а заносим в бд
        db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?)", (user, date, user_id))
#     print('пользователь: ', user, message.chat.first_name, message.chat.last_name, ' нажал старт')
#     %H:%M:%S время
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import *
from states.States import *
import time

# @dp.message_handler(commands=["start"], state="*", chat_type=["private"])
# async def start(message: types.Message, state: FSMContext):

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if db.get("SELECT id FROM users WHERE user_id = ?", (message.from_user.id,)) == None:
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (message.chat.username, int(time.time()), message.from_user.id, referrer_id,))
                try:
                    await bot.send_message(referrer_id, "💎Поздравляю, у вас плюс 1 реферал💎")
                except:
                    pass
            else:
                db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL)", (message.chat.username, int(time.time()), message.from_user.id,))
                await bot.send_message(message.from_user.id, "Нельзя зарегистрироваться по собственной ссылке")
        else:
            db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL)", (message.chat.username, int(time.time()), message.from_user.id,))
    await message.answer(
        f"Приветствуем вас в нашем <b>маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )
    print('пользователь: ', message.chat.username, message.chat.first_name, message.chat.last_name, ' нажал старт')
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
#       получаем айди рефера
        referrer_id = str(start_command[7:])
#       если ссылки рефера не обнаружено
        if str(referrer_id) != "":
#           проверка или человек не перешел по свой ссылке
            if str(referrer_id) != str(message.from_user.id):
                db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, ?, 0)", (message.chat.username, int(time.time()), message.from_user.id, referrer_id,))
                try:
#                    отправляем пользователю что по его ссылке перешли
                    await bot.send_message(referrer_id, "💎Поздравляю, у вас плюс 1 реферал💎")
                except:
                    pass
            else:
#               если пользователь попытался перейти по своей ссылке не регистрируясь при этом выпадает сообщение и регистрирует его как обычного юзера
                db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, 0)", (message.chat.username, int(time.time()), message.from_user.id,))
                await bot.send_message(message.from_user.id,
                                       "❌⚠️Отклонено. Причина:\nпопытка перехода по обственной ссылке⚠️❌"
                                       )
        else:
#           если пользователь не переходил по ссылке
            db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, 0)", (message.chat.username, int(time.time()), message.from_user.id,))
    await message.answer(
        f"Приветствуем вас в нашем <b>маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )

# записываем цену которую ввели
@dp.message_handler(state=StateMessage.translation)
async def add_translation(message: types.Message, state: FSMContext):   

    if message.text.isdigit() == False:
        await message.answer("❌Нельзя вводить ничего кроче числа❌")
    else:
        await state.update_data(translation=message.text)
        await message.answer("🪪Введите nickname пользователя🪪\n🔵пример: @lolzcoder_star🔵")
        await StateMessage.nickname.set()
    
# записываем пользователя которого указали    
@dp.message_handler(state=StateMessage.nickname)
async def add_username(message: types.Message, state: FSMContext):
    
    await state.update_data(nickname=message.text)
    await message.answer("❇️⚜️Введите условие сделки⚜️❇️\nпримечание: при каком условии вы хотите получить товар")
    await StateMessage.description.set()
    
@dp.message_handler(state=StateMessage.nickname)
async def add_description(message: types.Message, state: FSMContext):
    
    await state.update_data(description=message.text)
    await state.finish()
    
    
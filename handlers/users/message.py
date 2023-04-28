from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import *
from states.States import *
import time
from aiogram.dispatcher.filters import Text

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
                db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0)", (message.chat.username, int(time.time()), message.from_user.id, referrer_id,))
                try:
#                    отправляем пользователю что по его ссылке перешли
                    await bot.send_message(referrer_id, "💎Поздравляю, у вас плюс 1 реферал💎")
                except:
                    pass
            else:
#               если пользователь попытался перейти по своей ссылке не регистрируясь при этом выпадает сообщение и регистрирует его как обычного юзера
                db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, 0, 0, 0, 0, 0, 0)", (message.chat.username, int(time.time()), message.from_user.id,))
                await bot.send_message(message.from_user.id,
                                       "❌⚠️Отклонено. Причина:\nпопытка перехода по обственной ссылке⚠️❌"
                                       )
        else:
#           если пользователь не переходил по ссылке
            db.change(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, 0, 0, 0, 0, 0, 0)", (message.chat.username, int(time.time()), message.from_user.id,))
    await bot.send_photo(
        message.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"Приветствуем вас в нашем <b>маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )

# выход из состояний
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['остановись', 'cancel', 'выйти', 'выход', 'back', 'end', 'назад', 'конец', 'стоп', 'отмена'], ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_photo(
        message.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"✅Успешная отмена ввода",
        reply_markup=start_keyboard
    )

# записываем цену которую ввели
@dp.message_handler(state=StateMessage.translation)
async def add_translation(message: types.Message, state: FSMContext):   

# проверка хватает у юхера денег или нет
    subtraction_balance = db.get("SELECT balance FROM users WHERE user_id = ?", (message.from_user.id,))
    for subtraction_balance in subtraction_balance:
        pass
    if  message.text.replace(".", "", 1).isdigit() == False:
        await message.reply("🟥 Нельзя вводить ничего кроче числа 🟥")
    else:
        if subtraction_balance < float(message.text):
            await message.reply(f"🥲На вашем счету нету такой суммы\nУ вас на счету: {subtraction_balance}$")
        else:
            await state.update_data(translation=message.text)
            await message.answer("◻️Введите NickName пользователя\n◼Важно: вводить nickname без '@'\n🔸Пример ввода: lolzcoder_star")
            await StateMessage.nickname.set()
    
# записываем пользователя которого указали    
@dp.message_handler(state=StateMessage.nickname)
async def add_username(message: types.Message, state: FSMContext):
    
    user = db.get("SELECT login FROM users WHERE login = ?", (message.text,))
    if not user:
        await message.answer(f"🚷Пользователь с ником: @{message.text} не зарегистрирован🚷\n")
    else:
        await state.update_data(nickname=message.text)
        await message.answer(f"◽️Для потверждения NickName: @{message.text}\n🔸Введите NickName повторно")
        await StateMessage.userid.set()
    
# получаем по нику id пользователя   
@dp.message_handler(state=StateMessage.userid)
async def add_user_id(message: types.Message, state: FSMContext):
    
    data = await state.get_data()
    user_id = db.get("SELECT user_id FROM users WHERE login = ?", (data['nickname'],))
    if message.text != data['nickname']:
            await message.answer("🔸Введите NickName пользователя коректно🔸")
    else:
        await state.update_data(userid=user_id)
        await message.answer("⚪️Введите условие сделки⚫\n🔸Описание: при каком условии состоится сделка")
        await StateMessage.description.set()

@dp.message_handler(state=StateMessage.description)
async def add_description(message: types.Message, state: FSMContext):
    
    data = await state.get_data()
    if len(message.text) > 100:
            await message.answer("🟥Нельзя вводить более 100 символов🟥")
    else:
        await state.update_data(description=message.text)
        await message.answer(
            f"📣Отправить запрос на сделку пользователю: @{data['nickname']}?",
            reply_markup = InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton("🟢Подтвердить отправку", callback_data="endЕransaction"),
                InlineKeyboardButton("🔴Отменить", callback_data="backMenu_after_deal")
                )
            )
        await StateMessage.end.set()


# состояние кнопки пополнения
@dp.message_handler(state=Payment.currency)
async def add_currency(message: types.Message, state: FSMContext):

    summ = message.text
    if summ.replace(".", "", 1).isdigit() == False:
        await message.answer("🟥 <b>Нельзя вводить ничего кроче числа</b> 🟥")
    else:
        if float(summ) > 100000:
            await message.answer("Нельзя вводить сумму больше 100000")
        else:
            await state.update_data(currency=message.text)
            await message.answer("Выберите код валюты",
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text="USDT", callback_data="USDT"),
                InlineKeyboardButton(text="TRX", callback_data="TRX")
                )
            )
            await Payment.network.set()

# кнопка вывода
@dp.message_handler(state=PaymentСonclusion.currency)
async def add_currency(message: types.Message, state: FSMContext):


    if  message.text.replace(".", "", 1).isdigit() == False:
        await message.answer("🟥 Нельзя вводить ничего кроче числа 🟥")
    else:
        await state.update_data(currency=message.text)
        await message.answer("Ввыберите код валюты",
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text="USDT", callback_data="usdt")
                )
            )
        await PaymentСonclusion.network.set()

@dp.message_handler(state=PaymentСonclusion.amount)
async def add_amount(message: types.Message, state: FSMContext):

    await state.update_data(amount=message.text)
    await message.answer(
        "Для подтверждения операции нажмите Перейти к выводу",
        reply_markup = InlineKeyboardMarkup(row_width=True).add(
            InlineKeyboardButton("🟢Перейти к выводу", callback_data="confirmationwithdrawal"),
            )
        )
    await PaymentСonclusion.end.set()

@dp.message_handler(content_types=['photo'], state=AddNewGame.photo)
async def load_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await AddNewGame.namegame.set()
    await message.reply("Введите название игры")

@dp.message_handler(state=AddNewGame.namegame)
async def load_namegame(message: types.Message, state: FSMContext):
    await state.update_data(namegame=message.text)
    await AddNewGame.cengame.set()
    await message.reply("Укажите цену за аккаунт")

@dp.message_handler(state=AddNewGame.cengame)
async def load_cengame(message: types.Message, state: FSMContext):
    await state.update_data(cengame=message.text)
    await AddNewGame.loginaccount.set()
    await message.reply("Введите логин от аккаунта\nПользователь увидит его только после того как купит")

@dp.message_handler(state=AddNewGame.loginaccount)
async def load_login(message: types.Message, state: FSMContext):
    await state.update_data(loginaccount=message.text)
    await AddNewGame.password.set()
    await message.reply("Введите пароль от аккаунта\nПользователь увидит его только после того как купит")

@dp.message_handler(state=AddNewGame.password)
async def add_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    db.change("INSERT INTO games VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (data['photo'], data['namegame'], data['cengame'], data['loginaccount'], data['password'], message.from_user.id, message.from_user.username))
    await bot.send_photo(
        message.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"🟢Аккаунт успешно выставлен на рынок🟢",
        parse_mode=types.ParseMode.HTML,
        reply_markup=market_keyboard
    )
    await state.finish()
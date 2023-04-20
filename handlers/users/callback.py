from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from keyboards.keyboard import *
from states.States import *
from loader import dp, db, bot
import config as cfg
import datetime

@dp.callback_query_handler(text="profile_button")
async def process_profile_command(call: types.CallbackQuery):
    
    date_register = db.get("SELECT date_register FROM users WHERE user_id = ?", (call.from_user.id,))
    balance = db.get("SELECT balance FROM users WHERE user_id = ?", (call.from_user.id,))
    transactions = db.get("SELECT number_transactions FROM users WHERE user_id = ?", (call.from_user.id,))
    for balance in balance:
        pass
    for x in date_register:
        date = datetime.datetime.fromtimestamp(x).strftime('%d-%m-%Y')
    for transactions in transactions:
        pass
    
    await call.message.edit_text(
        f"👤Информация о пользователе: \n📃Логин пользователя: {call.from_user.username}\n⏳Дата регистрации: {date}\n👑Количество проведенных сделок: {transactions}\n💵Баланс: {balance}$\n⚖Сколько всего выведено в бота: 0$\n⚖Сколько всего введено в бота: 0$",
        parse_mode="html",
        reply_markup = profile_keyboard
    )
    
@dp.callback_query_handler(text="support_button")
async def process_support_command(call: types.CallbackQuery):
    await call.message.edit_text(
        f"👤 Контакты нашей поддержки:\n@wolfsblood550 - Главный администратор\n@lolzcoder_star - Директор\nПо всем вопросам обращаться к администратору, по поводу ошибок обращаться к деректору",
        parse_mode="html",
        reply_markup = support_keyboard
    )

@dp.callback_query_handler(text="add_balance_button")
async def process_add_balance_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '💲 Выберите способ оплаты:',
        parse_mode="html",
        reply_markup = add_money_keyboard
    )
    
@dp.callback_query_handler(text="withdraw_money_button")
async def process_withdraw_balance_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '💲 Выберите способ вывода:',
        parse_mode="html",
        reply_markup = withdraw_money_keyboard
    )
    
@dp.callback_query_handler(text="referal_system_button")
async def process_referal_command(call: types.CallbackQuery):
    await call.message.edit_text(
        f"🔗 Ваша реферальная ссылка: https://t.me/{cfg.BOT_NICKNAME}?start={call.from_user.id}",
        parse_mode="html",
        reply_markup = referal_system_keyboard
    )
    
@dp.callback_query_handler(text="guarantee_deal_button")
async def process_guarntee_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '▪ Создать сделку с пользователем ▫\n🔸Важно: Следуйте инструкции для предотвращения нежелательных ошибок',
        parse_mode="html",
        reply_markup = guarantee_deal_keyboard
    )
    
@dp.callback_query_handler(text="my_purchases_button")
async def process_purchases_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '🛒‍ Ваши покупки:\nПопробуйте вывести данные о покупках по айдишнику ',
        parse_mode="html",
        reply_markup = my_purchases_keyboard
    )
    
@dp.callback_query_handler(text="market_button")
async def process_market_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '📰 Выберите тематику',
        parse_mode="html",
        reply_markup = market_keyboard
    )   

#Кнопки рынка
    
@dp.callback_query_handler(text="accounts_button")
async def process_accounts_command(call: types.CallbackQuery):
    
    await call.message.edit_text(
          f"🔶Выберите действие: ",
         reply_markup = accounts_keyboard
     )

@dp.callback_query_handler(text="accounts")
async def all_products(call: types.CallbackQuery):
    
    data = db.get("SELECT * FROM products", (), False)
    await call.message.edit_text("◽️◼️◽️Список товаров по разделу аккаунты:◽️◼️◽️", reply_markup=genmarkup(data))  

    
@dp.callback_query_handler(text="manuals_button")
async def process_manuals_command(call: types.CallbackQuery):
    await call.message.edit_text(
        'Список всех товаров по выбранной вами тематике:',
        parse_mode="html",
        reply_markup = manuals_keyboard
    )
    
@dp.callback_query_handler(text="cancel_product", state=GoodsMarket.end)
async def process_manuals_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        'Список всех товаров по выбранной вами тематике:',
        parse_mode="html",
        reply_markup = manuals_keyboard
        )
    await state.finish()
# Процесс создания товара на рынок

@dp.callback_query_handler(text="add_your_product_button", state=None)
async def process_add_product_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Введите название товара:')
    await GoodsMarket.namegoods.set()
    
@dp.callback_query_handler(text="display_product", state=GoodsMarket.end)
async def end_creation(call: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    db.change(f"INSERT INTO products VALUES(NULL, ?, ?, ?, ?)", (data['namegoods'], data['description'], data['abouеseller'], data['price'],))
    await call.message.edit_text(
        f"Инфорамция о вашем товаре\nНазвание: {data['namegoods']}\nОписание: {data['description']}\nО продавце: {data['abouеseller']}\nЦена: {data['price']}$",
        reply_markup = products
        )
    await state.finish()
    
#Кнопки реферальной системы

@dp.callback_query_handler(text="your_referals_button")
async def process_your_referals_command(call: types.CallbackQuery):
    await call.message.edit_text(
        f"👨‍👩‍👧‍👦 Кол-во рефералов: {db.count_referals(call.from_user.id)}",
        parse_mode="html",
        reply_markup = your_referals_keyboard
    )

#КНОПКИ СДЕЛКИ С ГАРАНТОМ
    
# загрузка суммы   
@dp.callback_query_handler(text="buyer_button", state=None)
async def start_deal(call: types.CallbackQuery, state: FSMContext):

# если у пользователя нету денег он не сможет начать сделку
    subtraction_balance = db.get("SELECT balance FROM users WHERE user_id = ?", (call.from_user.id,))
    for subtraction_balance in subtraction_balance:
        pass
    if subtraction_balance <= 0:       
        await call.message.edit_text("Нельзя начать сделку с 0$ на счету\nС перва пополните счет",
                                     reply_markup = no_money
                                     )
    else:
        transaction_status = db.get("SELECT transaction_status FROM users WHERE user_id = ?", (call.from_user.id,))
        for i in transaction_status:
            pass
        if i == 1:
            await call.message.edit_text("⛔️Нельзя создавать более 1 активной сделки\n⛔️Завершите старую сделку", reply_markup = start_keyboard)
        else:       
            await call.message.edit_text("▫Введите сумму сделки:\n▪пример: 🔸5$ / 🔸$5.23\n◼Важно: вводить без знака '$'")
            await StateMessage.translation.set()

# окончание состояния
@dp.callback_query_handler(state=StateMessage.end, text=["endЕransaction"])
async def call_sss(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    
    await call.message.edit_text(
        f"▫Сумма сделки: {data['translation']}$\n◻NickName получателя: @{data['nickname']}\n⚪Условие сделки: {data['description']}",
        reply_markup = my_purchases_keyboard
    )
    money = data['translation']

# Когда пользователь начинает сделку ему присваивается статус сделки 1
    db.change("UPDATE users SET transaction_status = ? WHERE user_id = ?", (1, call.from_user.id))
    db.change("UPDATE users SET summ_input = ? WHERE user_id = ?", (money, call.from_user.id,))
    
    await bot.send_message(data['userid'][0],
                f"🔔Вам пришел новый запрос на сделку\n▫Cумма сделки: {data['translation']}$\n◻Отправитель: @{call.from_user.username}\n⚪Условие сделки: {data['description']}",
                reply_markup = InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton("🟩Подтвердить сделку", callback_data=f"done_{call.from_user.id}"),
                        InlineKeyboardButton("🟥Отказаться от сделки", callback_data=f"cencel_{call.from_user.id}")
                    )           
                )
    await state.finish()
    
@dp.callback_query_handler(filters.Regexp("done*"))
async def callback_query(call: types.CallbackQuery):
    
     # Получаем передаваемые параметры
    params = call.data.split("_")

    balance = db.get("SELECT balance FROM users WHERE user_id = ?", (params[1],))
    summ_input = db.get("SELECT summ_input FROM users WHERE user_id = ?", (params[1],))
    
#   когда пользователь принимает запрос, то у того кто отправил запрос списывается счет
    for balance in balance:
        pass
    for summ in summ_input:
        pass
    
    newsumm = balance - summ
    
    db.change("UPDATE users SET balance = ? WHERE user_id = ?", (newsumm, params[1],))
    username = db.get("SELECT login FROM users WHERE user_id = ?", (params[1],))
    for username in username:
        pass
    
    await call.message.edit_text(f"В ожидании завершения сделки с пользователем {username}")
    await bot.send_message(params[1],
                f"\n\n🟩 Пользователь {call.from_user.username} согласился на сделку",
                reply_markup=InlineKeyboardMarkup(row_width=2).add(
                        InlineKeyboardButton("Завершить сделку", callback_data=f"addbalance_{call.from_user.id}"),
                    )
                )
    
@dp.callback_query_handler(filters.Regexp("addbalance*"))
async def callback_query(call: types.CallbackQuery):
    
    params = call.data.split("_")
        
    replenishment = db.get("SELECT summ_input FROM users WHERE user_id = ?", (call.from_user.id,))
    user_recipient = db.get("SELECT balance FROM users WHERE user_id = ?", (params[1],))
    username = db.get("SELECT login FROM users WHERE user_id = ?", (params[1],))
    for replenishment in replenishment:
        pass
    for user_recipient in user_recipient:
        pass
    for username in username:
        pass
    await bot.send_message(params[1], f"Сделка с пользователем: {call.from_user.username} состоялась! ваш счет пополнен на {replenishment}$", reply_markup = start_keyboard)
    await call.message.edit_text(f"Сделка c пользователем {username} состоялась, с вашего счета списано: {replenishment}$", reply_markup = start_keyboard)
    
    newbalance = user_recipient + replenishment

    onenumber_transactions = db.get("SELECT number_transactions FROM users WHERE user_id = ?", (params[1],))
    twonumber_transactions = db.get("SELECT number_transactions FROM users WHERE user_id = ?", (call.from_user.id,))
    for onenumber_transactions in onenumber_transactions:
        pass
    for twonumber_transactions in twonumber_transactions:
        pass
    onenumber_transactions = onenumber_transactions + 1
    twonumber_transactions = twonumber_transactions + 1
    
    db.change("UPDATE users SET transaction_status = ? WHERE user_id = ?", (0, call.from_user.id,))
    db.change("UPDATE users SET balance = ? WHERE user_id = ?", (newbalance, params[1],))
    db.change("UPDATE users SET summ_input = ? WHERE user_id = ?", (0, call.from_user.id,))
    db.change("UPDATE users SET number_transactions = ? WHERE user_id = ?", (onenumber_transactions, params[1],))
    db.change("UPDATE users SET number_transactions = ? WHERE user_id = ?", (twonumber_transactions, call.from_user.id,))
    
@dp.callback_query_handler(filters.Regexp("cencel*"))
async def callback_query(call: types.CallbackQuery):
    
     # Получаем передаваемые параметры
    params = call.data.split("_")
    
    db.change("UPDATE users SET summ_input = ? WHERE user_id = ?", (0, params[1],))
    db.change("UPDATE users SET transaction_status = ? WHERE user_id = ?", (0, params[1],))
    username = db.get("SELECT login FROM users WHERE user_id = ?", (params[1],))
    for username in username:
        pass
    
    await call.message.edit_text(f"🟥Вы отклонили запрос на сделку с пользователем: {username}", reply_markup = start_keyboard)
    await bot.send_message(params[1], f"\n\n🟥 Пользователь: {call.from_user.username} отклонил сделку",
                                reply_markup=start_keyboard
    )

#   КНОПКИ НАЗАД

@dp.callback_query_handler(state=StateMessage.end, text=["backMenu_after_deal"]) 
async def process_backMenu_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        f"Приветствуем вас в <b>нашем маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )
    await state.finish() 

@dp.callback_query_handler(text="backMenu")
async def process_backMenu_command(call: types.CallbackQuery):
    await call.message.edit_text(
        f"Приветствуем вас в <b>нашем маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )

@dp.callback_query_handler(text="backReferalMenu")
async def process_backReferalMenu_command(call: types.CallbackQuery):
    await call.message.edit_text(
        f"🔗 Ваша реферальная ссылка: https://t.me/{cfg.BOT_NICKNAME}?start={call.from_user.id}",
        parse_mode="html",
        reply_markup = referal_system_keyboard
    )
 
@dp.callback_query_handler(text="backGuaranteeMenu")
async def process_backGuaranteeMenu_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '📬 Создайте заявку на сделку: ',
        parse_mode="html",
        reply_markup = guarantee_deal_keyboard
    )
    
@dp.callback_query_handler(text="backMarketMenu")
async def process_backMarketMenu_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '📰 Выберите тематику',
        parse_mode="html",
        reply_markup = market_keyboard
    )   

@dp.callback_query_handler(text="backProductMenu")
async def process_backProductlMenu_command(call: types.CallbackQuery):
    await call.message.edit_text(
        'Список всех товаров по выбранной вами тематике:',
        parse_mode="html",
        reply_markup = manuals_keyboard
    )
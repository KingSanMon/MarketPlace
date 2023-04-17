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
        '🛒Желаете создать заявку на сделку с пользователем?🛒',
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
        'Список всех товаров по выбранной вами тематике:',
        parse_mode="html",
        reply_markup = accounts_keyboard
    )
    
@dp.callback_query_handler(text="manuals_button")
async def process_manuals_command(call: types.CallbackQuery):
    await call.message.edit_text(
        'Список всех товаров по выбранной вами тематике:',
        parse_mode="html",
        reply_markup = manuals_keyboard
    )

@dp.callback_query_handler(text="add_your_product_button")
async def process_add_product_command(call: types.CallbackQuery):
    await call.message.edit_text(
        'Введите название товара:',
        parse_mode="html",
        reply_markup = add_your_product_keyboard
    )

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
    await call.message.edit_text("💵 Введите сумму сделки:\n🔵пример: 🔘20  🔘20.20🔵")
    await StateMessage.translation.set()

# окончание состояния
@dp.callback_query_handler(state=StateMessage.end, text=["endЕransaction"])
async def call_sss(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text(
        f"💵Сумма сделки: {data['translation']}$\n🪪ник получателя: @{data['nickname']}\n📄Описание сделки: {data['description']}",
        reply_markup = my_purchases_keyboard
    )
    await bot.send_message(data['userid'][0],
                f"Вам пришел новый запрос на сделку\n💵Cумма сделки: {data['translation']}$\n🪪Отправитель: @{call.from_user.username}\n📄Условие сделки: {data['description']}",
                reply_markup = InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton("Закрыть сделку", callback_data="endЕransaction_users")
                    )           
                )
    await state.finish()
    
    


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
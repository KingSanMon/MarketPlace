from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from keyboards.keyboard import *
from states.States import *
from loader import dp, db, bot
from datetime import datetime
import config as cfg

@dp.callback_query_handler(text="profile_button")
async def process_profile_command(call: types.CallbackQuery):
    await call.message.edit_text(
        f"👤Информация о пользователе: \n📃Логин пользователя: {call.from_user.username}\n⏳Дата регистрации: \n👑Количество проведенных сделок: 0\n💵Баланс: 0$\n⚖Сколько всего выведено в бота: 0$\n⚖Сколько всего введено в бота: 0$",
        parse_mode="html",
        reply_markup = profile_keyboard
    )
    
@dp.callback_query_handler(text="support_button")
async def process_support_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '👤 Контакты нашей поддержки',
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
        '👨‍👩‍👧‍👦 Выберите роль: ',
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
        '👨‍👩‍👧‍👦 Кол-во рефералов: 0',
        parse_mode="html",
        reply_markup = your_referals_keyboard
    )

#КНОПКИ СДЕЛКИ С ГАРАНТОМ
    
@dp.callback_query_handler(text="buyer_button")
async def process_buyer_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '💵 Введите сумму сделки:',
        parse_mode="html",
        reply_markup = buyer_keyboard
    )
    
@dp.callback_query_handler(text="seller_button")
async def process_seller_command(call: types.CallbackQuery):
    await call.message.edit_text(
        '💵 Введите сумму сделки:',
        parse_mode="html",
        reply_markup = seller_keyboard
    )

#   КНОПКИ НАЗАД

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
        '👨‍👩‍👧‍👦 Выберите роль: ',
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
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = InlineKeyboardMarkup(row_width=2)
start_keyboard.add(
        InlineKeyboardButton(text="💈 Рынок", callback_data="market_button"),
        ).add(
        InlineKeyboardButton(text="📋 Личный кабинет", callback_data="profile_button"),
        InlineKeyboardButton(text="💾 Мои покупки", callback_data="my_purchases_button"),
        InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="add_balance_button"),
        InlineKeyboardButton(text="💸 Вывод средств", callback_data="withdraw_money_button")
        ).add(
        InlineKeyboardButton(text="📊 Реферальная система", callback_data="referal_system_button")
        ).add(
        InlineKeyboardButton(text="📑 Создать сделку через гаранта", callback_data="guarantee_deal_button")
        ).add(
        InlineKeyboardButton(text="👨‍🎓 Поддержка", callback_data="support_button"),
        )

support_keyboard = InlineKeyboardMarkup(row_width=2)
support_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

profile_keyboard = InlineKeyboardMarkup(row_width=2)
profile_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

add_money_keyboard = InlineKeyboardMarkup(row_width=2)
add_money_keyboard.add(
    InlineKeyboardButton(text="₿ BTC", callback_data="add_btc_but"),
    InlineKeyboardButton(text="Ξ ETH", callback_data="add_eth_but"),
    InlineKeyboardButton(text="💲 USDT", callback_data="add_usdt_but"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

withdraw_money_keyboard = InlineKeyboardMarkup(row_width=2)
withdraw_money_keyboard.add(
    InlineKeyboardButton(text="₿ BTC", callback_data="add_btc_but"),
    InlineKeyboardButton(text="Ξ ETH", callback_data="add_eth_but"),
    InlineKeyboardButton(text="💲 USDT", callback_data="add_usdt_but"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

referal_system_keyboard = InlineKeyboardMarkup(row_width=2)
referal_system_keyboard.add(
    InlineKeyboardButton(text="👨‍👩‍👧‍👦 Ваши рефералы", callback_data="your_referals_button"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

your_referals_keyboard = InlineKeyboardMarkup(row_width=2)
your_referals_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backReferalMenu")
    )

guarantee_deal_keyboard = InlineKeyboardMarkup(row_width=2)
guarantee_deal_keyboard.add(
    InlineKeyboardButton(text="🟢 Создать сделку", callback_data="buyer_button"),
#     InlineKeyboardButton(text="🟠 Активные сделки", callback_data="activ_buyer_button"),
    InlineKeyboardButton(text="🔴 Вернуться в меню", callback_data="backMenu")
    )

buyer_keyboard = InlineKeyboardMarkup(row_width=2)
buyer_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backGuaranteeMenu")
    )

seller_keyboard = InlineKeyboardMarkup(row_width=2)
seller_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backGuaranteeMenu")
    )

my_purchases_keyboard = InlineKeyboardMarkup(row_width=2)
my_purchases_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )
return_menu = InlineKeyboardMarkup(row_width=2)
return_menu.add(
    InlineKeyboardButton(text="💢 Вернутся в главное меню", callback_data="backMenu_after_deal")
    )

market_keyboard = InlineKeyboardMarkup(row_width=2)
market_keyboard.add(
    InlineKeyboardButton(text="📌 Аккаунты", callback_data="accounts_button"),
    InlineKeyboardButton(text="📌 Мануалы", callback_data="manuals_button"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

accounts_keyboard = InlineKeyboardMarkup(row_width=2)
accounts_keyboard.add(
    InlineKeyboardButton(text="📦 Выставить свой товар", callback_data="add_your_product_button"),
    InlineKeyboardButton(text="📝 Перейти к товарам", callback_data="accounts"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMarketMenu")
    )

manuals_keyboard = InlineKeyboardMarkup(row_width=2)
manuals_keyboard.add(
    InlineKeyboardButton(text="📦 Выставить свой товар", callback_data="add_your_product_button"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMarketMenu")
    )

add_your_product_keyboard = InlineKeyboardMarkup(row_width=2)
add_your_product_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backProductMenu")
    )
no_money = InlineKeyboardMarkup(row_width=2)
no_money.add(
    InlineKeyboardButton(text="Вернутся в меню", callback_data="backMenu"),
    InlineKeyboardButton(text="Пополнить", callback_data="add_balance_button")
    )

products = InlineKeyboardMarkup(row_width=1)
products.add(
    InlineKeyboardButton(text="Вернутся к просмотру товаров", callback_data="accounts_button"),
    InlineKeyboardButton(text="Вернуться в меню", callback_data="backMenu")
    )

def genmarkup(data): # передаём в функцию data

    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 2 # кол-во кнопок в строке
    for i in data: # цикл для создания кнопок
        markup.add(InlineKeyboardButton(i[1], callback_data=i[2])) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton(text="💢 Назад", callback_data="accounts_button"))
    return markup #возвращаем клавиатуру
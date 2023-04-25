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

add_balance = InlineKeyboardMarkup(row_width=2)
add_balance.add(
    InlineKeyboardButton(text="💵Пополнить", callback_data="add_balance_users"),
    InlineKeyboardButton(text="💢Вернутся в меню", callback_data="backMenu")
    )

suppurt = InlineKeyboardMarkup(row_width=1)
suppurt.add(
    InlineKeyboardButton(text="👨‍🎓 Поддержка", callback_data="support_button")
    )

support_keyboard = InlineKeyboardMarkup(row_width=2)
support_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

profile_keyboard = InlineKeyboardMarkup(row_width=2)
profile_keyboard.add(
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

my_purchases_keyboard = InlineKeyboardMarkup(row_width=2)
my_purchases_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )


market_keyboard = InlineKeyboardMarkup(row_width=2)
market_keyboard.add(
    InlineKeyboardButton(text="📌 Аккаунты", callback_data="accounts_button"),
    InlineKeyboardButton(text="📌 Мануалы", callback_data="manuals_button"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )

accounts_keyboard = InlineKeyboardMarkup(row_width=2)
accounts_keyboard.add(
    InlineKeyboardButton(text="📦 Мои аккаунты", callback_data="useraccounts"),
    InlineKeyboardButton(text="📝 Перейти к товарам", callback_data="accounts"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMarketMenu")
    )

new_accounts = InlineKeyboardMarkup(row_width=2)
new_accounts.add(
    InlineKeyboardButton(text="❇️Добавить аккаунт", callback_data="add_new"),
    InlineKeyboardButton(text="💢Назад", callback_data="accounts_button")
    )

back_add_new = InlineKeyboardMarkup(row_width=2)
back_add_new.add(
    InlineKeyboardButton(text="🎮Игры", callback_data="add_new_accounts_game"),
    InlineKeyboardButton(text="☎️Стим", callback_data="add_new_accounts_steam")
    ).add(
    InlineKeyboardButton(text="💢Назад", callback_data="useraccounts")
    )

no_money = InlineKeyboardMarkup(row_width=2)
no_money.add(
    InlineKeyboardButton(text="💢Вернутся в меню", callback_data="backMenu"),
    InlineKeyboardButton(text="💵Пополнить", callback_data="add_balance_button")
    )

account_sections = InlineKeyboardMarkup(row_width=2)
account_sections.add(
    InlineKeyboardButton(text="🎮Игры", callback_data="games"),
    InlineKeyboardButton(text="☎️Стим", callback_data="wallets"),
    InlineKeyboardButton(text="💢Назад", callback_data="accounts_button")
    )


# def genmarkup(data): # передаём в функцию data

#     markup = InlineKeyboardMarkup() # создаём клавиатуру
#     markup.add(*[InlineKeyboardButton(button[1], callback_data=button[1]) for button in data])
#     markup.add(InlineKeyboardButton(text="💢 Назад", callback_data="accounts_button"))
#     return markup #возвращаем клавиатуру
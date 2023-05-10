from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator

# region основные кнопки меню
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
# endregion

def genmarkup(data): # передаём в функцию data

    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.add(*[InlineKeyboardButton(button[2], callback_data=f"item_{button[0]}") for button in data])
    markup.add(
        InlineKeyboardButton(text="💢 Назад", callback_data="accounts")
        )
    return markup #возвращаем клавиатуру

# region Рынок(Мои аккаунты, переход к товарам)
accounts_keyboard = InlineKeyboardMarkup(row_width=2)
accounts_keyboard.add(
    InlineKeyboardButton(text="📦 Мои товары", callback_data="useraccounts"),
    InlineKeyboardButton(text="📝 Перейти к товарам", callback_data="accounts"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )
# endregion

# region  Добавление аккаунта-мои аккаунты
new_accounts = InlineKeyboardMarkup(row_width=2)
new_accounts.add(
    InlineKeyboardButton(text="❇️Добавить товар", callback_data="add_new"),
    InlineKeyboardButton(text="🛄Мои товары", callback_data="my_accounts"),
    InlineKeyboardButton(text="💢Назад", callback_data="market_button")
    )
# endregion

# region Разделы при добавлении аккаунта
def AddProducts(data):
    markup = InlineKeyboardMarkup(row_width=1) # создаём клавиатуру
    markup.add(*[InlineKeyboardButton(button[1], callback_data=f"adprod_{button[0]}") for button in data])
    markup.add(
        InlineKeyboardButton(text="💢 Назад", callback_data="market_button")
        )
    return markup #возвращаем клавиатуру
# endregion

# region Список моих аккаунтов
def myaccount(data): # передаём в функцию data

    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.add(*[InlineKeyboardButton(button[2], callback_data=f"item_{button[0]}") for button in data])
    markup.add(
        InlineKeyboardButton(text="💢 Назад", callback_data="useraccounts")
        )
    return markup #возвращаем клавиатуру
# endregion

# region Кнопка назад на главное меню
profile_keyboard = InlineKeyboardMarkup(row_width=2)
profile_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )
# endregion

def magazin(data, page):
    page_size = 6
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*[InlineKeyboardButton(button[2], callback_data=f"item_{button[0]}") for button in data[start_index:end_index] ])
    if page > 1:
        markup.row(InlineKeyboardButton(text="⬅️", callback_data=f"bac_mag_{page-1}"))
    if end_index < len(data):
        markup.row(InlineKeyboardButton(text="➡️", callback_data=f"and_mag_{page+1}"))
    markup.add(InlineKeyboardButton(text="💢 Назад", callback_data="accounts"))
    return markup

# region Вывод всех купленных товаров юзера

# если товаров больше чем надо
def paginator(data, page):
    page_size = 6
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*[InlineKeyboardButton(button[2], callback_data=f"myprid_{button[0]}") for button in data[start_index:end_index] ])
    if page > 1:
        markup.row(InlineKeyboardButton(text="⬅️", callback_data=f"bac_str_{page-1}"))
    if end_index < len(data):
        markup.row(InlineKeyboardButton(text="➡️", callback_data=f"and_str_{page+1}"))
    markup.add(InlineKeyboardButton(text="💢 Назад", callback_data="backMenu"))
    return markup
# endregion

# region Пополнение баланса
add_balance = InlineKeyboardMarkup(row_width=2)
add_balance.add(
    InlineKeyboardButton(text="💵Пополнить", callback_data="add_balance_users"),
    InlineKeyboardButton(text="💢Вернутся в меню", callback_data="backMenu")
    )
# endregion

# region Вывод средств
autput_balance = InlineKeyboardMarkup(row_width=2)
autput_balance.add(
    InlineKeyboardButton(text="💵Вывести", callback_data="autput_balance_users"),
    InlineKeyboardButton(text="💢Вернутся в меню", callback_data="backMenu")
    )
# endregion

# region реферальная система
referal_system_keyboard = InlineKeyboardMarkup(row_width=2)
referal_system_keyboard.add(
    InlineKeyboardButton(text="👨‍👩‍👧‍👦 Ваши рефералы", callback_data="your_referals_button"),
    InlineKeyboardButton(text="💢 Назад", callback_data="backMenu")
    )
# endregion

suppurt = InlineKeyboardMarkup(row_width=1)
suppurt.add(
    InlineKeyboardButton(text="👨‍🎓 Поддержка", callback_data="support_button")
    )

your_referals_keyboard = InlineKeyboardMarkup(row_width=2)
your_referals_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="referal_system_button")
    )

guarantee_deal_keyboard = InlineKeyboardMarkup(row_width=2)
guarantee_deal_keyboard.add(
    InlineKeyboardButton(text="🟢 Создать сделку", callback_data="buyer_button"),
    InlineKeyboardButton(text="🔴 Вернуться в меню", callback_data="backMenu")
    )

my_purchases_keyboard = InlineKeyboardMarkup(row_width=2)
my_purchases_keyboard.add(
    InlineKeyboardButton(text="💢 Назад", callback_data="market_button")
    )

no_money = InlineKeyboardMarkup(row_width=2)
no_money.add(
    InlineKeyboardButton(text="💢Вернутся в меню", callback_data="backMenu"),
    InlineKeyboardButton(text="💵Пополнить", callback_data="add_balance_button")
    )


def sectionsAdd(data):
    markup = InlineKeyboardMarkup(row_width=1) # создаём клавиатуру
    markup.add(*[InlineKeyboardButton(button[1], callback_data=f"section_{button[0]}") for button in data])
    markup.add(
        InlineKeyboardButton(text="💢 Назад", callback_data="market_button")
        )
    return markup #возвращаем клавиатуру

# админ панель
def accountsReview(data):
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.add(*[InlineKeyboardButton(button[2], callback_data=f"baget_{button[0]}") for button in data])
    markup.add(
        InlineKeyboardButton(text="💢 Назад", callback_data="backAdmin_panel")
        )
    return markup #возвращаем клавиатуру

def reviewComplaints(data):
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.add(*[InlineKeyboardButton(button[1], callback_data=f"review_{button[0]}") for button in data])
    markup.add(
        InlineKeyboardButton(text="💢 Назад", callback_data="backAdmin_panel")
        )
    return markup #возвращаем клавиатуру

admin_start = InlineKeyboardMarkup(row_width=2)
admin_start.add(
    InlineKeyboardButton(text="📋Список жалоб", callback_data="complaints_button"),
    InlineKeyboardButton(text="🚷Бан пользователей", callback_data="ban_users"),
    InlineKeyboardButton(text="🛒Добавить раздел", callback_data="add_razdel"),
    InlineKeyboardButton(text="📦Товары для подтрвеждения", callback_data="market_buton_add")
    ).add(
    InlineKeyboardButton(text="💸Пополнить баланс пользователя", callback_data="admin_balance_users")
    )

admin_complaints_back = InlineKeyboardMarkup()
admin_complaints_back.add(
    InlineKeyboardButton(text="Вернутся к жалобам", callback_data="complaints_button")
    )

yes_no_button = InlineKeyboardMarkup(row_width=2)
yes_no_button.add(
    InlineKeyboardButton(text="✅Да", callback_data="amdin_add_balance"),
    InlineKeyboardButton(text="💢Назад", callback_data="backAdmin_panel")
    )

ban_users_button = InlineKeyboardMarkup(row_width=2)
ban_users_button.add(
    InlineKeyboardButton(text="Забанить", callback_data="baned_users"),
    InlineKeyboardButton(text="Разбанить", callback_data="unban_users"),
    InlineKeyboardButton(text="Назад", callback_data="backAdmin_panel")
    )
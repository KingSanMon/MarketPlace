from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from keyboards.keyboard import *
from states.States import *
from loader import dp, db, bot
from cryptomus import Client
from handlers.admin.message import admins
import config as cfg
import datetime

# region ключи для пополнениея и вывода средств
# на вывод
PAYOUT_KEY = 'Dt0xmkKOcb5AFPGLzV1T7A925pGAlAV2kNOxzzy6wKKSEw3iIWfCAmDgRK5bFUOuB130UuVS5CJCl1JkVNxra2LvlKlDkExD2d9OAu1wus2KsWKV6CsZ0XhZjTw219q1'
MERCHANT_UUID = 'e1c2e3c5-9e75-4438-a6f6-746a362d4bf6'

payout = Client.payout(PAYOUT_KEY, MERCHANT_UUID)

# на пополнение
PAYMENT_KEY = 'qd38AHmwZu9cIPVUDyfe3DZ2ezvWlkWuy5S2vv2jtoSJB8gC562ZFYfzeSphocBa8KTk3LB47cRTzzrNdb5CIRKbiTWSOy2AMettnI0YYPgI43aViJUnSbA0andEQsq8'

payment = Client.payment(PAYMENT_KEY, MERCHANT_UUID)
# endregion

# region Рынок
@dp.callback_query_handler(text="market_button")
async def process_market_command(call: types.CallbackQuery):

    with open(f"photos/bitoc.png", 'rb') as file:
        photo = types.InputMediaPhoto(file)
        await call.message.edit_media(media=photo)

    await call.message.edit_caption(
        f"❕<u><b>Чтобы выставить свой товар на площадку</b></u>\n💮Нажмите кнопку: Мои аккаунты\n----------------------------------------------------------------\n❕<u><b>Чтобы просмотреть весь имеющийся ассортимент</b></u>\n💮Нажмите на кнопку: Перейти к товарам",
        parse_mode=types.ParseMode.HTML,
        reply_markup=accounts_keyboard
    )

# region Добавление нового аккаунта-просмотр моих аккаунтов
@dp.callback_query_handler(text="useraccounts")
async def add_product(call: types.CallbackQuery):
    await call.message.edit_caption(
        f"🔮Выберите нужно вам действие",
        parse_mode=types.ParseMode.HTML,
        reply_markup=new_accounts
    )
# endregion

# region Добавление нового аккаунта-выбор раздела
@dp.callback_query_handler(text="add_new")
async def procces_add_accounts(call: types.CallbackQuery):
    data = db.get("SELECT * FROM sections", (), False)
    await call.message.edit_caption(
        f"💮Выберите раздел, к которому относится ваш продукт🛄",
        parse_mode=types.ParseMode.HTML,
        reply_markup=AddProducts(data)
    )
# endregion

# region Состояние добавления аккаунта игры
@dp.callback_query_handler(filters.Regexp("adprod*"), state="*")
async def add_new_accounts(call: types.CallbackQuery, state: FSMContext):
    
    data = call.data.split("_")[1]
    await state.update_data(sectionid=data)

    await AddNewGame.photo.set()
    await call.message.reply("Загрузите фотографию аккаунта")
# endregion

# region Информация об аккаунтах юзера
@dp.callback_query_handler(text="my_accounts")
async def info_my_accounts(call: types.CallbackQuery):
    data = db.get("SELECT * FROM games WHERE user_id = ?", (call.from_user.id,), False)
    await call.message.edit_caption(
        f"Список ваших аккаунтов:",
        parse_mode=types.ParseMode.HTML,
        reply_markup=myaccount(data)
    )
# endregion

# region Переход к товарам-выбор раздела
@dp.callback_query_handler(text="accounts")
async def all_products(call: types.CallbackQuery):
    
    data = db.get("SELECT * FROM sections", (), False)
    await call.message.edit_caption(
        f"◽️◼️◽️Выберите раздел◽️◼️◽️",
        parse_mode=types.ParseMode.HTML,
        reply_markup=sectionsAdd(data)
    )
# endregion

# region Список всех товаров на рынке по разделу
@dp.callback_query_handler(filters.Regexp("section*"))
async def buy(call, page=1):

    idsection = call.data.split("_")[1]

    data = db.get("SELECT * FROM games WHERE status = ? AND section_id = ?", (0, idsection), False)
    section = db.get("SELECT * FROM sections", (), False)

    if not data:
        await call.answer("Товаров нет на рынке")
    else:
        await call.message.edit_caption(
            f'Все товары на рынке:',
            parse_mode=types.ParseMode.HTML,
            reply_markup=magazin(data, page)
        )

async def next_purcha(call, page):

    idsection = call.data.split("_")[1]

    data = db.get("SELECT * FROM games WHERE status = ? AND section_id = ?", (0, idsection), False)

    await call.message.edit_caption(
        f'Все товары на рынке:',
        parse_mode=types.ParseMode.HTML,
        reply_markup=magazin(data, page)
    )

@dp.callback_query_handler(lambda call: call.data.startswith('and_mag_'))
async def next_pages(call):

    page = int(call.data.split('_')[2])
    await next_purcha(call, page)

@dp.callback_query_handler(lambda call: call.data.startswith('bac_mag_'))
async def prev_pages(call):
    
    page = int(call.data.split('_')[2])
    await buy(call, page)
# endregion

# region Инфомрация о товаре
@dp.callback_query_handler(filters.Regexp("item*"))
async def view_info_products(call: types.CallbackQuery):

    item = call.data.split("_")[1]

    userinfo = db.get("SELECT * FROM games WHERE id = ?", (item,))
    user = db.get("SELECT * FROM users WHERE user_id = ?", (userinfo[6],))

    estimations = db.get("SELECT estimation FROM estimations WHERE userid = ?", (user[3],), False)
    if estimations:
        average_rating = sum(estimation[0] for estimation in estimations) / len(estimations)
    else:
        average_rating = 0

    if userinfo[6] == call.from_user.id:

        await call.message.delete()

        confedicialpassword = userinfo[5][:-5] + '******'
        confediciallogin = userinfo[4][:-4] + '*****'

        if userinfo[8] == 1:
            statys = '🔶На рассмотрении'
        else:
            statys = '🟢Товар одобрен'
        await bot.send_photo(
        call.from_user.id, userinfo[1],
        f"🎮 Название: <b>{userinfo[2]}</b>\n---------------------------------------\n💰 Цена: <b>{userinfo[3]}</b>$\n---------------------------------------\n👤 Продавец: <b>@{userinfo[7]}</b>\n---------------------------------------\n📝 Количество сделок: <b>{user[6]}</b>\n---------------------------------------\n📝 Пароль: {confedicialpassword}\n---------------------------------------\n🪪 Логин: {confediciallogin}\n---------------------------------------\nСтатус: <b>{statys}</b>",
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"accounts")
            )
        )
    else:

        await call.message.delete()

        await bot.send_photo(
        call.from_user.id, userinfo[1],
        f"🎮 Название: <b>{userinfo[2]}</b>\n---------------------------------------\n💰 Цена: <b>{userinfo[3]}</b>$\n---------------------------------------\n👤 Продавец: <b>@{userinfo[7]}</b>\n---------------------------------------\n📝 Количество сделок: <b>{user[6]}</b>\n---------------------------------------\n⭐️ Рейтинг продавца: {average_rating}",
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="🛒 Купить", callback_data=f"add_garant_{userinfo[0]}"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"accounts")
            )
        )
# endregion

# region Сделка через гаранта на рынке
@dp.callback_query_handler(filters.Regexp("add_garant*"))
async def garant(call: types.CallbackQuery):
    try:
        item = call.data.split("_")

        products = db.get("SELECT * FROM games WHERE id = ?", (item[2],))
        summ_sdel = products[3]
        userid = products[6]

        mybalance = db.get("SELECT * FROM users WHERE user_id = ?", (call.from_user.id,))

        if mybalance[8] == 1:
            await call.message.edit_caption("Нельзя иметь более 1 активной сделки", reply_markup=profile_keyboard)
        else:
            if mybalance[5] < products[3]:
                await call.message.edit_caption("На вашем счету не достаточно средств", reply_markup=add_balance)
            else:

                db.change("UPDATE games SET status = ? WHERE id = ?", (3, products[0]))

                await call.message.edit_caption("Ожидание сделки...")
                await bot.send_message(userid,
                    f"🔔Вам пришел новый запрос на сделку\n▫Cумма сделки: {summ_sdel}$\n◻Отправитель: @{call.from_user.username}\nОписание: покупка товара -{products[2]}-",
                    reply_markup = InlineKeyboardMarkup(row_width=1).add(
                            InlineKeyboardButton("🟩Подтвердить сделку", callback_data=f"next_{call.from_user.id}_{item[2]}"),
                            InlineKeyboardButton("🟥Отказаться от сделки", callback_data=f"minys_{call.from_user.id}_{products[0]}")
                        )
                    )
    except:
        await call.message.answer("Товара нету в наличии")


@dp.callback_query_handler(filters.Regexp("next*"))
async def garant_al(call: types.CallbackQuery):
    item = call.data.split("_")

    users = db.get("SELECT * FROM users WHERE user_id = ?", (item[1],))
    products = db.get("SELECT * FROM games WHERE id = ?", (item[2],))

    await call.message.edit_text(f"🟢Вы согласились на сделку с @{users[1]}🟢")

    newbalance = users[5] - products[3]
    
    db.change("UPDATE users SET transaction_status = ? WHERE user_id = ?", (1, item[1]))
    db.change("UPDATE users SET balance = ? WHERE user_id = ?", (newbalance, item[1]))

    await bot.send_message(item[1], f"🟩Продавец {call.from_user.username} согласился на сделку🟩\nЛогин от аккаунта: {products[4]}\nПароль: {products[5]}",
                    reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text="🤝 Закрыть сделку", callback_data=f"endp_{products[0]}_{call.from_user.id}"),
                InlineKeyboardButton(text="✍🏿 Открыть чат", url=f"https://t.me/{call.from_user.username}"),
                InlineKeyboardButton(text="🗣 Открыть спор", callback_data=f"spor_{products[0]}_{call.from_user.id}")
            )
        )
    
    db.change("INSERT INTO confirmation VALUES(?, ?, ?, ?, ?, ?)", (products[0], products[1], products[2], products[3], products[4], products[5]))
    db.change("DELETE FROM games WHERE id=?", (item[2],))

@dp.callback_query_handler(filters.Regexp("spor*"))
async def spor(call: types.CallbackQuery):

    diskushion = call.data.split("_")

    users = db.get("SELECT * FROM users WHERE user_id = ?", (diskushion[2],))
    products = db.get("SELECT * FROM confirmation WHERE id = ?", (diskushion[1],))

    await call.message.edit_text(f"💸Меня обманул пользователь: @{users[1]}\n❗️На сумму: {products[3]}$\n📩Отпрвить жалобу?",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="📥 Отпрвить", callback_data=f"send_{diskushion[2]}_{diskushion[1]}"),
            InlineKeyboardButton(text="⭕️ Закрыть сделку", callback_data=f"endp_{products[0]}_{call.from_user.id}")
            )
        )

@dp.callback_query_handler(filters.Regexp("send*"))
async def add_db(call: types.CallbackQuery):

    warning = call.data.split("_")

    products = db.get("SELECT * FROM confirmation WHERE id = ?", (warning[2],))

    await call.message.delete()
    await bot.send_photo(call.from_user.id,
    photo=types.InputFile(open("photos/image.png", "rb")),
    caption="✅Жалоба успешно отправлена на рассмотрение администраторам\n💤Ожидайте.....",
    reply_markup=start_keyboard
    )

    db.change("INSERT INTO dispute VALUES(NULL, ?, ?, ?)", (call.from_user.id, products[3], warning[1]))
    db.change("UPDATE users SET transaction_status = ? WHERE user_id = ?", (0, call.from_user.id))
    db.change("DELETE FROM confirmation WHERE id = ?", (warning[2],))

@dp.callback_query_handler(filters.Regexp("minys"))
async def garant_adl(call: types.CallbackQuery):

    debag = call.data.split("_")

    users = db.get("SELECT * FROM users WHERE user_id = ?", (debag[1],))

    await call.message.edit_text(f"🔴Вы отказались от сделки c @{users[1]}🔴")
    await bot.send_message(debag[1], "🟥Продавец отказался от сделки🟥")
    
    db.change("UPDATE games SET status = ? WHERE id = ?", (0, debag[2]))

@dp.callback_query_handler(filters.Regexp("endp*"))
async def garant_end(call: types.CallbackQuery):

    item = call.data.split("_")

    users = db.get("SELECT * FROM users WHERE user_id = ?", (item[2],))
    users_deal = db.get("SELECT * FROM users WHERE user_id = ?", (call.from_user.id,))
    products = db.get("SELECT * FROM confirmation WHERE id = ?", (item[1],))

    transaction_statusone = users[6] + 1
    transaction_statustwo = users_deal[6] + 1

    await call.message.edit_text(
        f"❇️Сделка с пользователем @{users[1]} завершена успешно\n💠С вашего счета списано: {products[3]}$\nПоставьте оценку продавцу",
        reply_markup=InlineKeyboardMarkup(row_width=2).add(
                        InlineKeyboardButton(text="Поставить", callback_data=f"postav_{users[0]}"),
                        InlineKeyboardButton(text="Выйти в меню", callback_data="backMenus")
                    )
        )
    newbalance = users[5] + products[3]

    db.change("INSERT INTO my_buy_products VALUES(NULL, ?, ?, ?, ?, ?)", (call.from_user.id, products[2], products[4], products[5], products[3]))
    db.change("UPDATE users SET balance = ?, number_transactions = ? WHERE user_id = ?", (newbalance, transaction_statusone, item[2],))
    db.change("UPDATE users SET transaction_status = ?, number_transactions = ? WHERE user_id = ?", (0, transaction_statustwo, call.from_user.id))

    await bot.send_message(item[2], f"Сделка с пользователем @{call.from_user.username} завершена успешно\nВаш счет пополнен на {products[3]}$")

    db.change("DELETE FROM confirmation WHERE id = ?", (item[1],))

@dp.callback_query_handler(filters.Regexp("postav*"), state=None)
async def add_once(call: types.CallbackQuery):

    data = call.data.split("_")

    keyboard = InlineKeyboardMarkup(row_width=2)
    for barbi in range(1, 6):
        keyboard.add(*[InlineKeyboardButton(str(barbi), callback_data=f"barber_{barbi}_{data[1]}")])
    await call.message.edit_text(
        "Поставьте оценку от 1 до 5",
        reply_markup=keyboard
    )
    await Estimation.estimation.set()

@dp.callback_query_handler(filters.Regexp("barber*"), state=Estimation.estimation)
async def process_estimation(call: types.CallbackQuery, state: FSMContext):

    estimation = call.data.split("_")

    users = db.get("SELECT * FROM users WHERE id = ?", (estimation[2],))

    if estimation[1].isdigit() and 1 <= int(estimation[1]) <= 5:

        await call.message.delete()
        await bot.send_photo(
            call.from_user.id,
            photo=types.InputFile(open("photos/image.png", "rb")),
            caption=f"Вы поставили оценку {estimation[1]}, пользователю: @{users[1]}\nСпасибо за голосова", reply_markup=start_keyboard)

        db.change("INSERT INTO estimations VALUES(?, ?)", (estimation[1] , users[3]))

        await state.finish()
    else:
        await call.answer("Пожалуйста, выберите оценку от 1 до 5")
# endregion

# endregion

# region Личный кабинет
@dp.callback_query_handler(text="profile_button")
async def process_profile_command(call: types.CallbackQuery):
    
    users = db.get("SELECT * FROM users WHERE user_id = ?", (call.from_user.id,))
    date = datetime.datetime.fromtimestamp(users[2]).strftime('%d.%m.%Y')

    estimations = db.get("SELECT * FROM estimations WHERE userid = ?", (call.from_user.id,), False)

    if estimations:
        average_rating = sum(estimation[0] for estimation in estimations) / len(estimations)
    else:
        average_rating = 0

    await call.message.edit_caption(
        f"👤Информация о пользователе\n----------------------------------------------\n📃Логин пользователя: <code>{call.from_user.username}</code>\n⏳Дата регистрации: <u>{date}</u>\n👑Количество проведенных сделок: {users[6]}\n----------------------------------------------\n⭐️ Рейтинг: <b>{average_rating}</b>\n----------------------------------------------\n💵<b>Баланс: <code>{users[5]}</code>$</b>\n----------------------------------------------\n⚖Сколько всего введено в бота: {users[9]}$\n⚖Сколько всего выведено с бота: 0$",
        parse_mode=types.ParseMode.HTML,
        reply_markup=profile_keyboard
    )
# endregion

# region Информация о покупках
@dp.callback_query_handler(text="my_purchases_button")
async def show_purchases(call, page=1):

    data = db.get("SELECT * FROM my_buy_products WHERE user_id = ?", (call.from_user.id,), False)
    if not data:
        await call.message.edit_caption("У вас еще нету покупок", reply_markup=profile_keyboard)
    else:
        await call.message.edit_caption(
            f'🛒‍ Ваши покупки:',
            parse_mode=types.ParseMode.HTML,
            reply_markup=paginator(data, page)
        )

async def next_purchases(call, page):
    data = db.get("SELECT * FROM my_buy_products WHERE user_id = ?", (call.from_user.id,), False)
    await call.message.edit_caption(
        f'🛒‍ Ваши покупки:',
        parse_mode=types.ParseMode.HTML,
        reply_markup=paginator(data, page)
    )

@dp.callback_query_handler(lambda call: call.data.startswith('and_str_'))
async def next_page(call):
    page = int(call.data.split('_')[2])
    await next_purchases(call, page)

@dp.callback_query_handler(lambda call: call.data.startswith('bac_str_'))
async def prev_page(call):
    page = int(call.data.split('_')[2])
    await show_purchases(call, page)
# endregion 

# region Меню пополнение баланса
@dp.callback_query_handler(text="add_balance_button")
async def procces_pop_balance(call: types.CallbackQuery):

    await call.message.edit_caption(
        '💳 <i>Пополнение баланса</i>\n❓<u><b>Что бы отменить ввод, напишите "отмена"</b></u>\n<b>⚠️Что бы перейти к пополнению баланса</b>\n<b>⚠️Нажмите пополнить</b>',
        parse_mode="html",
        reply_markup = add_balance
    )
# endregion

# region Состояние пополнения счета юзера
@dp.callback_query_handler(text="add_balance_users", state=None)
async def process_add_balance_command(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()
    await call.message.answer(
        '💲Введите сумму пополнения:',
        parse_mode="html"
    )
    await Payment.currency.set()

@dp.callback_query_handler(text="USDT", state=Payment.network)
async def add_network_usdt(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(network="USDT")
    await call.message.edit_text("Выберите код блокчейна",
        reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="TRON", callback_data="TRON")
            )
        )
    await Payment.amount.set()

@dp.callback_query_handler(text="TRX", state=Payment.network)
async def add_network_trx(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(network="TRX")
    await call.message.edit_text("Выберите код блокчейна",
        reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="TRON", callback_data="TRON")
            )
        )
    await Payment.amount.set()

@dp.callback_query_handler(text="TRON", state=Payment.amount)
async def add_amount(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(amount="TRON")
    await call.message.edit_text("Сгенерируйте ссылку",
        reply_markup=InlineKeyboardMarkup(row_width=True).add(
            InlineKeyboardButton(text="Сгенерировать ссылку", callback_data="replenishment")
            )
        )
    await Payment.end.set()

# получение ссылки для пополнения счета
@dp.callback_query_handler(text="replenishment", state=Payment.end)
async def adding_funds_account(call: types.CallbackQuery, state: FSMContext):

    number = db.get("SELECT * FROM order_id", (), False)
    update = number[0][1]
    update_number = update+1
    data = await state.get_data()

    data_payment = {
    'amount': data['currency'],
    'currency': "USD",
    'network': data['amount'],
    'order_id': f"{update}",
    'url_return': 'https://example.com/return',
    'url_callback': 'https://example.com/callback',
    'is_payment_multiple': False,
    'lifetime': '7200',
    'to_currency': data['network']
    };

    result = payment.create(data_payment)
    result_url = result["url"]

    db.change("UPDATE order_id SET number = ?", (update_number,))

    await call.message.edit_text(
        f"Для оплаты перейдите на сайт",
        reply_markup = InlineKeyboardMarkup(row_width=1).add(
                       InlineKeyboardButton("Перейти для пополения", url=f"{result_url}"),
                       InlineKeyboardButton("Проверить оплату", callback_data=f"{update}_ch_{data['currency']}")
                    )
    )
    await state.finish()

@dp.callback_query_handler(filters.Regexp("ch"))
async def pay_moment(call: types.CallbackQuery):
#     # Проверка платежа
    params = call.data.split("_")
    data = {
        "uuid": "a7c0caec-a594-4aaa-b1c4-77d511857594",
        "order_id": f"{params[0]}"
    }

    result_p = payment.info(data)

    if result_p["payment_status"] == 'paid':
        await bot.send_photo(call.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"✅ Платеж прошел успешно, ваш баланс пополнен на: {params[2]}$",
        reply_markup = my_purchases_keyboard
        )

        total_received_balance = db.get("SELECT balance, total_received, referrer_id, number_deposits FROM users WHERE user_id = ?", (call.from_user.id,))

        if total_received_balance[2] != None:

            if total_received_balance[3] == 0:

                referrer = db.get("SELECT balance FROM users WHERE user_id = ?", (total_received_balance[2],))

                balance_referrer = float(params[2]) * 0.05
                new_referrer = float(referrer[0]) + balance_referrer
                number_deposits = total_received_balance[3] + 1
                total_received = total_received_balance[1] + float(params[2])
                balance = total_received_balance[0] + float(params[2])

                db.change("UPDATE users SET balance = ?, total_received = ?, number_deposits = ? WHERE user_id = ?", (balance, total_received, number_deposits, call.from_user.id))
                db.change("UPDATE users SET balance = ? WHERE user_id = ?", (new_referrer, total_received_balance[2]))

            else:

                total_received = total_received_balance[1] + float(params[2])
                balance = total_received_balance[0] + float(params[2])

                db.change("UPDATE users SET balance = ?, total_received = ? WHERE user_id = ?", (balance, total_received, call.from_user.id))

        else:

            total_received = total_received_balance[1] + float(params[2])
            balance = total_received_balance[0] + float(params[2])

            db.change("UPDATE users SET balance = ?, total_received = ? WHERE user_id = ?", (balance, total_received, call.from_user.id))

    elif result_p["payment_status"] == 'check':
        await bot.send_message(call.from_user.id, "♻️Платеж создан. Ожидание пополнения")
    else:
        await bot.send_message(call.from_user.id, "♻️ Платеж не найден")
# endregion

# region Меню вывода средств
@dp.callback_query_handler(text="withdraw_money_button")
async def payments_procces(call: types.CallbackQuery):

    await call.message.edit_caption(
        '💳 <i>Вывод средств</i>\n❓<u><b>Что бы отменить ввод, напишите "отмена"</b></u>\n<b>⚠️Что бы перейти к выводу средств</b>\n<b>⚠️Нажмите вывести</b>',
        parse_mode="html",
        reply_markup = autput_balance
    )
# endregion

# region Состояние вывода средств
@dp.callback_query_handler(text="autput_balance_users", state=None)
async def process_withdraw_balance_command(call: types.CallbackQuery):

    await call.message.reply(
        '💲Введите сумму вывода:',
        parse_mode="html"
    )
    await PaymentСonclusion.amount.set()

@dp.callback_query_handler(text="usdt", state=PaymentСonclusion.currency)
async def add_currency(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(currency="USDT")
    await call.message.edit_text(
        "Выберите сетевой код блокчейна",

        reply_markup=InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="TRON", callback_data="trons")
            )
        )
    await PaymentСonclusion.network.set()

@dp.callback_query_handler(text="trons", state=PaymentСonclusion.network)
async def add_network(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(network="TRON")
    await call.message.edit_text("Введите свой кошелек",)
    await PaymentСonclusion.address.set()

@dp.callback_query_handler(text="confirm", state=PaymentСonclusion.end)
async def output_balance(call: types.CallbackQuery, state: FSMContext):
    
    balance = db.get("SELECT * FROM users WHERE user_id = ?", (call.from_user.id,))
    order = db.get("SELECT number FROM order_id", ())[0]
    print(order)
    output = await state.get_data()

    if float(output['amount']) > balance[5]:
        await call.message.edit_text(f"у вас на кошельке нету суммы: {output['amount']}$")
    else:
        data = {
        'amount': output['amount'],
        'currency': output['currency'],
        'network': output['network'],
        'order_id': order,
        'address': output['address'],
        'is_subtract': '1',
        'url_callback': 'https://example.com/callback'
        }

        new_order = float(order) + 1
        db.change("UPDATE order_id SET number = ?", (new_order,))

        result = payout.create(data)
        await call.message.edit_text("Непредвиденная ошибка\nВидимо какие то данные заполнены не верно\nПожалуйста обратитесь к администратору", reply_markup=suppurt)
    await state.finish()
# endregion

# region Реферальная система
@dp.callback_query_handler(text="referal_system_button")
async def process_referal_command(call: types.CallbackQuery):

    await call.message.edit_caption(
        caption=f"🔗 Ваша реферальная ссылка: <code>https://t.me/{cfg.BOT_NICKNAME}?start={call.from_user.id}</code>",
        parse_mode="html",
        reply_markup = referal_system_keyboard
    )

@dp.callback_query_handler(text="your_referals_button")
async def process_your_referals_command(call: types.CallbackQuery):

    await call.message.edit_caption(
        f"👨‍👩‍👧‍👦 Кол-во рефералов: {db.count_referals(call.from_user.id)}",
        parse_mode="html",
        reply_markup = your_referals_keyboard
    )
# endregion

# region Сделка через гаранта
@dp.callback_query_handler(text="guarantee_deal_button")
async def process_guarntee_command(call: types.CallbackQuery):

    with open(f"photos/bitoc.png", 'rb') as file:
        photo = types.InputMediaPhoto(file)
        await call.message.edit_media(media=photo)

    await call.message.edit_caption(
        f"▪ Создать сделку с пользователем ▫\n🔸Важно: Следуйте инструкции для предотвращения нежелательных ошибок",
        parse_mode=types.ParseMode.HTML,
        reply_markup=guarantee_deal_keyboard
    )
# endregion

# region Состояние сделки через гаранта
@dp.callback_query_handler(text="buyer_button", state=None)
async def start_deal(call: types.CallbackQuery, state: FSMContext):

# если у пользователя нету денег он не сможет начать сделку
    subtraction_balance = db.get("SELECT balance FROM users WHERE user_id = ?", (call.from_user.id,))[0]
    if subtraction_balance <= 0:       
        with open(f"photos/bitoc.png", 'rb') as file:
            photo = types.InputMediaPhoto(file)
            await call.message.edit_media(media=photo)

        await call.message.edit_caption(
            f"💢Нельзя начать сделку с 0$ на счету\n💵Пополните счет",
            parse_mode=types.ParseMode.HTML,
            reply_markup=no_money
        )
    else:
        transaction_status = db.get("SELECT transaction_status FROM users WHERE user_id = ?", (call.from_user.id,))[0]
        if transaction_status == 1:
            await call.message.edit_caption("⛔️Нельзя создавать более 1 активной сделки\n⛔️Завершите старую сделку", reply_markup = start_keyboard)
        else:
            await call.message.delete()
            await call.message.answer("▫Введите сумму сделки:\n▪пример: 🔸5$ / 🔸$5.23\n◼Важно: вводить без знака '$'")
            await StateMessage.translation.set()

@dp.callback_query_handler(state=StateMessage.end, text=["endЕransaction"])
async def call_sss(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    await call.message.edit_text(
        f"▫Сумма сделки: {data['translation']}$\n◻NickName получателя: @{data['nickname']}\n⚪Условие сделки: {data['description']}",
        parse_mode=types.ParseMode.HTML,
        reply_markup=my_purchases_keyboard
    )

    db.change("UPDATE users SET transaction_status = ?, summ_input = ? WHERE user_id = ?", (1, data['translation'], call.from_user.id))
    
    await bot.send_message(data['userid'][0],
                f"🔔Вам пришел новый запрос на сделку\n▫Cумма сделки: {data['translation']}$\n◻Отправитель: @{call.from_user.username}\n⚪Условие сделки: {data['description']}",
                reply_markup = InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton("🟩Подтвердить сделку", callback_data=f"done_{call.from_user.id}_{data['translation']}"),
                        InlineKeyboardButton("🟥Отказаться от сделки", callback_data=f"cencel_{call.from_user.id}")
                    )           
                )
    await state.finish()
# endregion

# region подтверждение сделки
@dp.callback_query_handler(filters.Regexp("done*"))
async def garant_sistem_yes(call: types.CallbackQuery):
    
     # Получаем передаваемые параметры
    params = call.data.split("_")

    balance = db.get("SELECT balance, summ_input FROM users WHERE user_id = ?", (params[1],))
#   когда пользователь принимает запрос, то у того кто отправил запрос списывается счет    
    newsumm = balance[0] - balance[1]
    
    db.change("UPDATE users SET balance = ? WHERE user_id = ?", (newsumm, params[1],))
    username = db.get("SELECT login, user_id FROM users WHERE user_id = ?", (params[1],))
    
    await call.message.edit_text(
        f"В ожидании завершения сделки с пользователем @{username[0]}",
        reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text="✍🏿 Открыть чат", url=f"https://t.me/{username[0]}")
            )
        )
    
    await bot.send_message(params[1],
                f"\n\n🟩 Пользователь {call.from_user.username} согласился на сделку",
                reply_markup=InlineKeyboardMarkup(row_width=2).add(
                        InlineKeyboardButton(text="🤝Завершить сделку", callback_data=f"addbalance_{call.from_user.id}"),
                        InlineKeyboardButton(text="✍🏿 Открыть чат", url=f"https://t.me/{call.from_user.username}"),
                        InlineKeyboardButton(text="Открыть спор", callback_data=f"dataget_{username[1]}")
                    )
                )
    
@dp.callback_query_handler(filters.Regexp("dataget_*"))
async def dataget(call: types.CallbackQuery):

    data = call.data.split("_")[1]

    cheater = db.get("SELECT * FROM users WHERE user_id = ?", (data,))
    users = db.get("SELECT * FROM users WHERE user_id = ?", (call.from_user.id,))

    await call.message.answer(
        f"Меня обманул пользователь {cheater[1]}, на сумму {cheater[7]}",
        reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text="📥 Отпрвить", callback_data=f"fraud_{cheater[3]}")
            )
        )

@dp.callback_query_handler(filters.Regexp("fraud*"))
async def flaud(call: types.CallbackQuery):

    data = call.data.split("_")[1]

    await call.message.answer("Lf FLlwerk;fkwr")

    cheater = db.get("SELECT * FROM users WHERE user_id = ?", (data,))
    print(call.from_user.id, cheater[7], cheater[3])
    db.change("INSERT INTO dispute VALUES(NULL, ?, ?, ?)", (call.from_user.id, cheater[7], cheater[3]))

@dp.callback_query_handler(filters.Regexp("addbalance*"))
async def if_garant_sistem(call: types.CallbackQuery):
    
    params = call.data.split("_")
        
    replenishment = db.get("SELECT summ_input FROM users WHERE user_id = ?", (call.from_user.id,))[0]
    user_recipient = db.get("SELECT balance, login FROM users WHERE user_id = ?", (params[1],))

    await call.message.delete()
    await bot.send_photo(params[1], photo=types.InputFile(open("photos/image.png", "rb")), caption=f"Сделка с пользователем: {call.from_user.username} состоялась! ваш счет пополнен на {replenishment}$", reply_markup = start_keyboard)
    await bot.send_photo(
        call.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"Сделка c пользователем {user_recipient[1]} состоялась, с вашего счета списано: {replenishment}$", reply_markup = start_keyboard)
    
    newbalance = user_recipient[0] + replenishment

    onenumber_transactions = db.get("SELECT number_transactions FROM users WHERE user_id = ?", (params[1],))[0]
    twonumber_transactions = db.get("SELECT number_transactions FROM users WHERE user_id = ?", (call.from_user.id,))[0]

    onenumber_transactions = onenumber_transactions + 1
    twonumber_transactions = twonumber_transactions + 1
    
    db.change("UPDATE users SET transaction_status = ?, summ_input = ?, number_transactions = ? WHERE user_id = ?", (0, 0, twonumber_transactions, call.from_user.id,))
    db.change("UPDATE users SET balance = ?, number_transactions = ? WHERE user_id = ?", (newbalance, onenumber_transactions, params[1],))
# endregion

# region отказ от сделки 
@dp.callback_query_handler(filters.Regexp("cencel*"))
async def garans_sistem(call: types.CallbackQuery):
    
     # Получаем передаваемые параметры
    params = call.data.split("_")
    
    db.change("UPDATE users SET summ_input = ? WHERE user_id = ?", (0, params[1],))
    db.change("UPDATE users SET transaction_status = ? WHERE user_id = ?", (0, params[1],))
    username = db.get("SELECT * FROM users WHERE user_id = ?", (params[1],))
    
    await bot.send_photo(
        call.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"🟥Вы отклонили запрос на сделку с пользователем: {username[1]}", reply_markup = start_keyboard)
    await bot.send_photo(params[1], photo=types.InputFile(open("photos/image.png", "rb")), caption=f"\n\n🟥 Пользователь: {call.from_user.username} отклонил сделку",
                                reply_markup=start_keyboard
    )
# endregion

# region поддержка
@dp.callback_query_handler(text="support_button")
async def process_support_command(call: types.CallbackQuery):

    await call.message.edit_caption(
        f"👤 Контакты нашей поддержки:\n-------------------------------------------------------------\n@shshshgsuw2 - Администратор\n-------------------------------------------------------------\nВ случае возникновения какой либо ошибки\nОбращайтесь к администратору",
        parse_mode=types.ParseMode.HTML,
        reply_markup=profile_keyboard
    )
# endregion

# region кнопки назад
@dp.callback_query_handler(state=StateMessage.end, text=["backMenu_after_deal"]) 
async def back_menu(call: types.CallbackQuery, state: FSMContext):

    await bot.send_photo(
        call.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"Приветствуем вас в <b>нашем маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode="html",
        reply_markup = start_keyboard
    )
    await state.finish() 

@dp.callback_query_handler(text="backMenu")
async def back_menu_deal(call: types.CallbackQuery):

    with open(f"photos/image.png", 'rb') as file:
        photo = types.InputMediaPhoto(file)
        await call.message.edit_media(media=photo)

    await call.message.edit_caption(
        f"Приветствуем вас в <b>нашем маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode=types.ParseMode.HTML,
        reply_markup=start_keyboard
    )

@dp.callback_query_handler(text="backMenus")
async def process_backMenu_command(call: types.CallbackQuery):

    await call.message.delete()
    await bot.send_photo(
        call.from_user.id,
        photo=types.InputFile(open("photos/image.png", "rb")),
        caption=f"Приветствуем вас в <b>нашем маркете!</b> Выберете пункт меню, необходимый вам!🤑",
        parse_mode=types.ParseMode.HTML,
        reply_markup=start_keyboard
    )
 
@dp.callback_query_handler(text="backGuaranteeMenu")
async def process_backGuaranteeMenu_command(call: types.CallbackQuery):

    await call.message.edit_text(
        '📬 Создайте заявку на сделку: ',
        parse_mode="html",
        reply_markup = guarantee_deal_keyboard
    )
# endregion

@dp.callback_query_handler(filters.Regexp("myprid"))
async def callback_query(call: types.CallbackQuery):

    review = call.data.split("_")[1]
    myprod = db.get("SELECT * FROM my_buy_products WHERE id = ?", (review,))
    await call.message.edit_caption(f"Название: {myprod[2]}\nЛогин: {myprod[3]}\nПароль: {myprod[4]}\nЦена: {myprod[5]}",
        reply_markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="⬅️Назад", callback_data="my_purchases_button")
            )
        )
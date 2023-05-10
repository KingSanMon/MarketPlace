from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import *
from filters.filters import *
from states.States import *
import re

# Главное меню-------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="backAdmin_panel")
async def menu(call: types.CallbackQuery):
	await call.message.edit_text(
        f"💎 Добро пожаловать <b><u>{call.from_user.username}</u></b>, вы получили доступ к админ панели\n⚙️ Чем займемся сегодня?",
        parse_mode="html",
        reply_markup=admin_start)
# Главное меню конец-------------------------------------------------------------------------------------

# Жалобы от пользователей--------------------------------------------------------------------------------
@dp.callback_query_handler(text="complaints_button")
async def complaint(call: types.CallbackQuery):
	complaints = db.get("SELECT * FROM dispute", (), False)
	await call.message.edit_text(f"Общее количество жалоб: {len(complaints)}", reply_markup=reviewComplaints(complaints))

@dp.callback_query_handler(filters.Regexp("review*"))
async def add_merket(call: types.CallbackQuery):

	review = call.data.split("_")[1]

	dispute = db.get("SELECT * FROM dispute WHERE id = ?", (review,))
	users = db.get("SELECT * FROM users WHERE user_id = ?", (dispute[1],))
	cheater = db.get("SELECT * FROM users WHERE user_id = ?", (dispute[3],))

	await call.message.edit_text(
		f"📋Новая жалоба\n➖➖➖➖➖➖➖➖\nОт: <b>{users[1]}</b>\n➖➖➖➖➖➖➖➖\nНа: <b>{cheater[1]}</b>\n➖➖➖➖➖➖➖➖\nСумма: {dispute[2]}$",
		reply_markup=InlineKeyboardMarkup(row_width=2).add(
			InlineKeyboardButton(text="🔴Забанить", callback_data=f"bancheat_{cheater[3]}_{users[0]}_{dispute[2]}"),
    		InlineKeyboardButton(text="⬅️Назад", callback_data="complaints_button"),
    		InlineKeyboardButton(text="🟢Закрыть сделку", callback_data=f"complite_sdel_{dispute[0]}")
			)
		)
# Жалобы от пользователей конец--------------------------------------------------------------------------

# Забанить пользователя----------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Regexp("bancheat"))
async def baned_cheater(call: types.CallbackQuery):

	ban = call.data.split("_")

	cheater = db.get("SELECT * FROM users WHERE user_id = ?", (ban[1],))
	users = db.get("SELECT * FROM users WHERE id = ?", (ban[2],))

	db.change("UPDATE users SET ban = ? WHERE user_id = ?", (1, ban[1],))

	await call.message.edit_text(f"⛔️Пользователь {cheater[1]} забанен⛔️", reply_markup=admin_start)
	await bot.send_message(ban[1], "❌❌Ваш аккаунт был забанен❌❌")
	await bot.send_message(users[3], f"🟢Пользователь: {cheater[1]} был забанен\nВам на счет вернули: {ban[3]}$")
# Забанить пользователя конец----------------------------------------------------------------------------

# Закрыть сделку-----------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Regexp("complite_sdel*"))
async def complute(call: types.CallbackQuery):

	complite = call.data.split("_")[2]
	
	dispute = db.get("SELECT * FROM dispute WHERE id = ?", (complite,))
	users = db.get("SELECT * FROM users WHERE user_id = ?", (dispute[1],))
	cheater = db.get("SELECT * FROM users WHERE user_id = ?", (dispute[3],))

	newbalance = cheater[5] + dispute[2]
	db.change("UPDATE users SET balance = ?, summ_input = ?, transaction_status = ? WHERE user_id = ?", (newbalance, 0, 0, dispute[3],))

	await bot.send_message(users[3], f"Администратор закрыл сделку с: {cheater[1]}")
	await bot.send_message(cheater[3], f"Администратор закрыл сделку с: {users[1]}")

	db.change("DELETE FROM dispute WHERE id = ?", (complite,))

	await call.message.edit_text("Жалоба устранена", reply_markup=admin_complaints_back)

# Закрыть сделку конец-----------------------------------------------------------------------------------

# Бан пользователей--------------------------------------------------------------------------------------
@dp.callback_query_handler(text="ban_users")
async def button_ban(call: types.CallbackQuery):
	await call.message.edit_text(f"<b>{call.from_user.username}</b>\nВыберите действие которое вам нужно",
	reply_markup=ban_users_button)
# Бан пользователей конец--------------------------------------------------------------------------------

# Добавить раздел----------------------------------------------------------------------------------------
@dp.callback_query_handler(text="add_razdel", state=None)
async def add_sectiom(call: types.CallbackQuery):
	await call.message.edit_text("Введите название раздела")
	await Addsections.name.set()

# Добавить раздел конец----------------------------------------------------------------------------------

# Одобрение товара на рынок------------------------------------------------------------------------------
@dp.callback_query_handler(text="market_buton_add")
async def add_market(call: types.CallbackQuery):
	data = db.get("SELECT * FROM games WHERE status = ?", (1,), False)
	await call.message.edit_text(
		"Все товары которые находятся в ожидании",
		reply_markup=accountsReview(data)
		)

@dp.callback_query_handler(filters.Regexp("baget*"))
async def add_merkets(call: types.CallbackQuery):
	try:
		idprod = call.data.split("_")[1]
		userinfo = db.get("SELECT * FROM games WHERE id = ?", (idprod,))
		confedicialpassword = userinfo[5][:-5] + '******'
		confediciallogin = userinfo[4][:-4] + '*****'
		await bot.send_photo(
			call.from_user.id, userinfo[1],
			 f"🎮 Название: <b>{userinfo[2]}</b>\n---------------------------------------\n💰 Цена: <b>{userinfo[3]}</b>$\n---------------------------------------\n👤 Продавец: <b>@{userinfo[7]}</b>\n---------------------------------------\n📝 Пароль: {confedicialpassword}\n---------------------------------------\n🪪 Логин: {confediciallogin}",
			 parse_mode="html",
			 reply_markup=InlineKeyboardMarkup(row_width=2).add(
			 	InlineKeyboardButton(text="🟢Одобрить", callback_data=f"approval_{idprod}"),
			 	InlineKeyboardButton(text="🔴Отклонить", callback_data=f"reject_{idprod}")
			 	)
			)
	except:
		await call.message.answer("Товар не найден")

@dp.callback_query_handler(filters.Regexp("approval*"))
async def add_merket(call: types.CallbackQuery):
	idprod = call.data.split("_")[1]
	messuser = db.get("SELECT * FROM games WHERE id = ?", (idprod,))
	await bot.send_message(messuser[6], f"🟢Ваш товар: {messuser[2]}\n🟢Одобрен")
	await call.message.delete()
	await call.message.answer("Товар одобрен")
	db.change("UPDATE games SET status = ? WHERE id = ?", (0, idprod))

@dp.callback_query_handler(filters.Regexp("reject*"))
async def delete_market(call: types.CallbackQuery):
	idprod = call.data.split("_")[1]
	messuser = db.get("SELECT * FROM games WHERE id = ?", (idprod,))
	await bot.send_message(messuser[6], f"🔴Ваш товар: {messuser[2]}\n🔴Не одобрен")
	await call.message.delete()
	await call.message.answer("Не одорено")
	db.change("DELETE FROM games WHERE id = ?", (idprod,))
# Одобрение товара на рынок конец------------------------------------------------------------------------

# пополнение админами баланс юзера ----------------------------------------------------------------------
@dp.callback_query_handler(text="admin_balance_users")
async def add_balance(call: types.CallbackQuery):
	await call.message.edit_text("Вы точно желаете пополнить счет пользователю?", reply_markup=yes_no_button)

@dp.callback_query_handler(text="amdin_add_balance", state=None)
async def add_balance(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text("Введите логин пользователя")
	await AddBalanceUsers.login.set()

@dp.callback_query_handler(text="add_balance_yes", state=AddBalanceUsers.end)
async def add_balance_user(call: types.CallbackQuery, state: FSMContext):

	data = await state.get_data()
	users = db.get("SELECT * FROM users WHERE login = ?", (data['login'],))
	new_balance = users[5] + float(data['depositAmount'])

	db.change("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, users[3]))
	await call.message.edit_text(
		f"Вы успешно пополнили баланс {data['login']}\nНа сумму: {data['depositAmount']}$",
		reply_markup=admin_start
		)
	await bot.send_message(users[3], f"💠 Вам пришел подгон от админа\n💎 На сумму: {data['depositAmount']}$")
	await state.finish()
# пополнение админами баланс юзера конец----------------------------------------------------------------
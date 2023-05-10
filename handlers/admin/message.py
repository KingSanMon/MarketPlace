from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import *
from filters.filters import *
from states.States import *
from config import admins
from aiogram.dispatcher.filters import Text

# Основные команды-----------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands='admin')
@dp.message_handler(Text(equals=['admin', 'администратор']))
async def admin_panel(message: types.Message):
	if message.from_user.id in admins:
		print(f"-------Админ {message.from_user.username} зашел навести суету---------")
		await message.answer(
        f"💎 Добро пожаловать <b><u>{message.from_user.username}</u></b>, вы получили доступ к админ панели\n⚙️ Чем займемся сегодня?",
        parse_mode="html",
        reply_markup=admin_start)
	else:
		print(f"/////Не санкционированная попытка входа {message.from_user.username}////////")
		await message.answer("🚷У вас не достаточно прав")

@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['стоп'], ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
	if message.from_user.id in admins:
	    current_state = await state.get_state()
	    if current_state is None:
	        return
	    await state.finish()
	    await message.answer("✅Успешная отмена ввода", reply_markup=admin_start)
	else:
		await message.answer("🚷У вас не достаточно прав")
# Основные команды конец-----------------------------------------------------------------------------------------------------------------------

# пополнение админами баланс юзера --------------------------------
# Логин пользователя и его данные
@dp.message_handler(state=AddBalanceUsers.login)
async def add_login(message: types.Message, state: FSMContext):

	user = db.get("SELECT * FROM users WHERE login = ?", (message.text,))

	if not user:
 		await message.answer(f"Нету пользователя @{message.text}")
	else:
		await state.update_data(login=message.text)
		await message.answer("Введите сумму пополнения")
		await AddBalanceUsers.depositAmount.set()

# Сумма поплнения
@dp.message_handler(state=AddBalanceUsers.depositAmount)
async def add_deposit(message: types.Message, state: FSMContext):

	if  message.text.replace(".", "", 1).isdigit() == False:
		await message.reply("Нельзя вводить ничего кроче числа")
	else:
		await state.update_data(depositAmount=message.text)
		data = await state.get_data()

		await message.answer(
			f"Подтвердаете пополнение счета пользователя: @{data['login']}?\nНа сумму: {data['depositAmount']}$",
			reply_markup=InlineKeyboardMarkup(row_width=2).add(
				InlineKeyboardButton(text="Да", callback_data="add_balance_yes")
				)
			)
		await AddBalanceUsers.end.set()
# пополнение админами баланс юзера конец---------------------------

# Добавление раздела------------------------------------------------------------------
@dp.message_handler(state=Addsections.name)
async def add_section(message: types.Message, state: FSMContext):
	await state.update_data(name=message.text)
	await message.answer(f"Успешно добавили раздел: {message.text}", reply_markup=admin_start)
	db.change("INSERT INTO sections VALUES(NULL, ?)", (message.text,))
	await state.finish()
# Добавление раздела конец------------------------------------------------------------
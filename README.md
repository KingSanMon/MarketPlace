# python-aiogram-model
python-aiogram-model

States Example
```python
class Registration(StatesGroup):
     login = State()
     password = State()
     end = State()
```

Handlers Example Without States
```python
@dp.message_handler(commands=["start"], state="*", chat_type=["private"])
async def start(message: types.Message, state: FSMContext):
  
  await bot.answer("Please write login")
  await Registration.login.set()
  
@dp.callback_query_handler(text=["test"], state="*")
async def call_message(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "test"
    )
```

Handlers Example States
```python
@dp.message_handler(state=Registration.login, content_types=["text"])
async def get_message(message: types.Message, state: FSMContext):

  await state.update_data(login=message.text)
  await bot.answer("Please write password")
  await Registration.password.set()
  
@dp.message_handler(state=Registration.password, content_types=["text"])
async def get_message(message: types.Message, state: FSMContext):

  await state.update_data(password=message.text)
  await bot.answer(
    "Please write password",
    reply_markup = InlineKeyboardMarkup(row_width=1).add(
      InlineKeyboardButton(
          "📋 End Registration",
          callback_data="endRegistration"
      )
    )
  await Registration.end.set()
  
@dp.callback_query_handler(state=WorkRequests.sendAdmin, text=["endRegistration"])
async def call_sss(call: types.CallbackQuery, state: FSMContext):
  data = await state.get_data()
  await call.message.edit_text(
    f"Login: {data['login']} | Password: {data['password']}"
  )
  await state.finish()
  
```

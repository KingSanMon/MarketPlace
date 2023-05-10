from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler 
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message, CallbackQuery
from loader import db
import time
import keyboards.keyboard as kb

user_ban_status = {}

class UserBanned(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):

        if not message.from_user.username:
            await message.answer("Я не могу тебя пустить дальше, у тебя нет @username")
            raise CancelHandler

        user_id = message.from_user.id
        if user_id in user_ban_status:
            is_banned = user_ban_status[user_id]
        else:
            is_banned = db.get("SELECT ban FROM users WHERE user_id = ?", (user_id, ))[0]
            user_ban_status[user_id] = is_banned

        if is_banned == 1:
            await message.answer('🔥 Вы заблокированы')
            raise CancelHandler

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        pass

        if not call.from_user.username:
            await call.answer("<b>Я не могу тебя пустить дальше, у тебя нет @username</b>", show_alert=True)
            raise CancelHandler

        user_id = call.from_user.id
        if user_id in user_ban_status:
            is_banned = user_ban_status[user_id]
        else:
            is_banned = db.get("SELECT ban FROM users WHERE user_id = ?", (user_id, ))[0]
            user_ban_status[user_id] = is_banned

        if is_banned == 1:
            await call.answer('🔥 Вы заблокированы')
            raise CancelHandler
            
            
class UserSpam(LifetimeControllerMiddleware):
    MAX_MESSAGES_PER_MINUTE = 5
    TIME_RANGE_IN_SECONDS = 60

    def __init__(self):
        super().__init__()

        self.user_messages_count = {}

    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id
        current_time = time.time()

        if user_id not in self.user_messages_count:
            self.user_messages_count[user_id] = []

        # Удаление старых сообщений из списка
        self.user_messages_count[user_id] = list(filter(
            lambda timestamp: timestamp > current_time - self.TIME_RANGE_IN_SECONDS,
            self.user_messages_count[user_id]))

        # Добавление нового сообщения в список
        self.user_messages_count[user_id].append(current_time)

        # Если количество сообщений превышает лимит, отменяем обработку сообщения
        if len(self.user_messages_count[user_id]) > self.MAX_MESSAGES_PER_MINUTE:
            await message.answer("Слишком много сообщений. Подождите немного и попробуйте еще раз.")
            raise CancelHandler

class UserUpdateLogin(BaseMiddleware):

    # если пользователь решит поменять логин
    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        try:
            user_id = call.from_user.id
            username = call.from_user.username
            userlogin = db.get("SELECT login FROM users WHERE user_id = ?", (user_id,))
            for userlogin in userlogin:
                pass
            if userlogin != call.from_user.username:
                db.change("UPDATE users SET login = ? WHERE user_id = ?", (username, user_id,))
                await call.message.answer('<b>🔥Ваш login был обновлен, вы дальше можете использовать бота</b>')
        except:
            pass
            raise CancelHandler
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from config import *


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return int(message.from_user.id) == ADMIN
    
    async def check_two(self, call: types.CallbackQuery):
        return int(call.from_user.id) == ADMIN

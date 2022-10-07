import sqlite3
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db





# class MessageState(StatesGroup):
#     message1 = State()
#     message2 = State()
#     message3 = State()
#     message4 = State()


async def start(message: types.Message):
    hello_mes = """Привет, ты пользуешься ботом, 
в котором можно добавлять количество принятых и выданных заказов и просматривать их за определенный день"""
    id_tlg = message.from_user.id
    name = message.from_user.full_name
    user_name = message.from_user.username
    await db.add_users(id_tlg=id_tlg, fullname=name, user_name=user_name)
    await message.answer(hello_mes)


async def help_c(message: types.Message):
    help = """/start - используйте чтобы начать работу и перезапустить\n
    /help - справочная информация, поможет понять как работает бот\n
    /accept - добавление принятых заказов в БД\n
    /given - добавление выданных заказов в БД\n
    /get - получение по информации по количеству заказов за определенный день
    БД - база данных"""
    await message.answer(help)

async def get_your_id(message: types.Message):
    await message.answer(f"Hello {message.from_user.id}")




def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(get_your_id, commands="hello", state="*")
    dp.register_message_handler(help_c, commands="help", state="*")


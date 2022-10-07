from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from loader import dp, db
from handlers.users.message_s import MessageState


async def start_insert(message: types.Message):
    await message.answer("""Напишите в сообщение, которое ваш пвз и количество заказов за сегодняшний день.\n 
    Добавление произведется в два шага. Введите ваш ПВЗ формате английскими буквами 'kzn-1'.\n
    Пишите маленькими буквами и без кавычек.""")
    await MessageState.message1.set()


async def pvz_insert_pvz(message: types.Message, state: FSMContext):
    await state.update_data(pvz_data=message.text)
    await message.answer("Напиши количество заказов за сегодняшний день в формате: 220\nМожешь вводить данные:")
    await MessageState.message2.set()


async def pvz_insert_db(message: types.Message, state: FSMContext):
    await state.update_data(amount_data=message.text)
    data = await state.get_data()
    pvz_info = data['pvz_data']
    amount_info = int(data['amount_data'])
    await db.add_orders(pvz=pvz_info, amount=amount_info)
    await message.answer(f"Добавлено в базу данных информация: {pvz_info} и {amount_info}")
    await state.finish()


def register_handlers_insert(dp: Dispatcher):
    dp.register_message_handler(start_insert, commands="message", state="*")
    dp.register_message_handler(pvz_insert_pvz, state=MessageState.message1)
    dp.register_message_handler(pvz_insert_db, state=MessageState.message2)

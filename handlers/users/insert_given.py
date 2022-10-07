
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from loader import dp, db
from handlers.users.message_s import MessageState


async def start_given(message: types.Message):
    await message.answer("""Напишите в сообщение ваш пвз и количество выданных заказов за сегодняшний день.\n 
    Добавление произведется в два шага. Введите ваш ПВЗ формате английскими буквами 'kzn-1'.\n
    Пишите маленькими буквами и без кавычек.""")
    await MessageState.message7.set()


async def given_pvz(message: types.Message, state: FSMContext):
    await state.update_data(pvz_data=message.text)
    await message.answer("Напиши количество выданных заказов за сегодняшний день в формате: 220\nМожешь вводить данные:")
    await MessageState.message8.set()


async def given_ord(message: types.Message, state: FSMContext):
    await state.update_data(amount_data=message.text)
    data = await state.get_data()
    pvz_info = data['pvz_data']
    amount_info = int(data['amount_data'])
    await db.add_orders_given(f_pvz=pvz_info, amount=amount_info)
    await message.answer(f"Добавлено в базу данных информация: {pvz_info} и {amount_info}.\n"
                         f"Вы заработали за выданные заказы: {amount_info * 0.5}")
    await state.finish()


def register_handlers_given(dp: Dispatcher):
    dp.register_message_handler(start_given, commands="given", state="*")
    dp.register_message_handler(given_pvz, state=MessageState.message7)
    dp.register_message_handler(given_ord, state=MessageState.message8)

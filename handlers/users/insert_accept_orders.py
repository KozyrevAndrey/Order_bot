

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from loader import db
from handlers.users.message_s import MessageState


async def accept_start(message: types.Message):
    await message.answer("""Напишите в сообщение ваш пвз и количеством принятых заказов за сегодняшний день.\n 
Добавление произведется в два шага. Сейчас нужно ввести ваш ПВЗ формате английскими буквами 'kzn-1'.\n
Пишите маленькими буквами и без кавычек.
    """)
    await MessageState.message5.set()


async def accept_pvz(message: types.Message, state: FSMContext):
    await state.update_data(pvz_data_acc=message.text)
    await message.answer("Напиши количество принятых заказов за сегодняшний день в формате: 220\nМожешь вводить данные:")
    await MessageState.message6.set()


async def accept_add(message: types.Message, state: FSMContext):
    await state.update_data(orders_data_acc=message.text)
    data = await state.get_data()
    pvz_info = data['pvz_data_acc']
    amount_info = int(data['orders_data_acc'])
    print(f"""
    {amount_info}, {pvz_info}
    """)
    await db.add_orders_acc(f_pvz=pvz_info, amount=amount_info)
    await message.answer(f"Добавлено в базу данных информация: {pvz_info} и {amount_info}.\n"
                         f"Вы заработали за принятые заказы: {amount_info * 1}")
    await state.finish()


def register_handlers_acc(dp: Dispatcher):
    dp.register_message_handler(accept_start, commands="accept", state="*")
    dp.register_message_handler(accept_pvz, state=MessageState.message5)
    dp.register_message_handler(accept_add, state=MessageState.message6)


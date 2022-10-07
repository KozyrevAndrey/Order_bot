
# select_ord means select_orders

from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db



from handlers.users.message_s import MessageState


"""
OLD VERSION
"""

async def select_all(message: types.Message):
    await message.answer("""Напиши пвз, который хочешь найти и день за который хочешь получить количество заказов.
    Напиши пвз в формате: kzn-1. Здесь вводи данные:""")
    await MessageState.message3.set()


async def select_pvz(message: types.Message, state: FSMContext):
    await state.update_data(pvz_select=message.text)
    await message.answer("Напиши день за который хочешь заказы.\n"
                         "Формат: 2022-09-29\n"
                         "Можешь вводить данные:")
    await MessageState.message4.set()


async def get_info_amount(message: types.Message, state: FSMContext):
    await state.update_data(date_select=message.text)
    data_a = await state.get_data()
    pvz_dec, date_v = data_a["pvz_select"], data_a["date_select"]
    #date_v = data_a["date_select"]

    date_dec = datetime.strptime(date_v, "%Y-%m-%d").date()
    order = await db.select_orders_try(pvz=pvz_dec,
                                       insert_day=date_dec)
    print(f"""
        _______________________
        {order}
        _______________________
        """)
    await message.answer(f"В {data_a['pvz_select']} за {data_a['date_select']} было {str(order)} заказов")
    await state.finish()


def register_handlers_select_ord(dp: Dispatcher):
    dp.register_message_handler(select_all, commands='amount', state="*")
    dp.register_message_handler(select_pvz, state=MessageState.message3)
    dp.register_message_handler(get_info_amount, state=MessageState.message4)
from aiogram import types

from loader import dp

@dp.message_handlers()
async def bot_echo(message: types.Message):
    chat_id = message.from_user.id
    text = message.text

    from loader import bot

    await bot.send_message(chat_id=chat_id, text=text)

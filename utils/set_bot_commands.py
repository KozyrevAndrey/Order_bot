from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начало работы"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/accept", description="Сохрани принятые заказы"),
        BotCommand(command="/given", description="Сохрани выданные заказы"),
        BotCommand(command="/get", description="Узнай количество всех заказов"),
        BotCommand(command="/hello", description="Hello"),
    ]
    await bot.set_my_commands(commands)


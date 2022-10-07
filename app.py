import asyncio
import logging


from handlers.users.insert_accept_orders import register_handlers_acc
from handlers.users.get_amount import register_handlers_get
from handlers.users.insert_given import register_handlers_given
from loader import dp, db, bot


from handlers.users.start import register_handlers_start

from utils.set_bot_commands import set_commands

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    await db.create()

    register_handlers_start(dp)
    register_handlers_acc(dp)
    register_handlers_given(dp)
    register_handlers_get(dp)

    try:
        await db.create_table_users()
        await db.create_table_pvz()
        await db.create_table_d_acc()
        await db.create_table_d_g()
    except Exception as err:
        print(err)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())


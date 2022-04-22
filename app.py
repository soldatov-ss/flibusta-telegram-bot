from aiogram import executor

from config import CHAT_ID
from loader import dp, db
from utils.set_bot_command import set_admin_commands


async def on_startup(dispatcher):
    import middlewares, handlers
    from utils.set_bot_command import set_default_commands
    await db.create()
    await db.create_tables()
    await set_default_commands(dp)
    await set_admin_commands(dp, chat_id=CHAT_ID)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

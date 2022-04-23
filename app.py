from aiogram import executor

from config import CHAT_ID, GROUP_ID
from loader import dp, db


async def on_startup(dispatcher):
    import middlewares, handlers
    from utils.set_bot_command import set_default_commands, set_admin_commands, set_group_commands
    await db.create()
    await db.create_tables()
    await set_default_commands(dp)
    await set_admin_commands(dp, chat_id=CHAT_ID)
    await set_group_commands(dp, GROUP_ID)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

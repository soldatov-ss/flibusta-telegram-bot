import asyncio

from aiogram import Dispatcher

from config import ADMIN_ID, GROUP_ID
from integrations.telegraph import FileUploader, TelegraphService
from loader import dp, db, bot
from middlewares import IntegrationMiddleware
from middlewares.session import SQLAlchemySessionMiddleware
from utils.parsing.general import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'mysql+mysqlconnector://mysql:password@172.20.0.2:3306/database'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Add the SQLAlchemy session middleware
dp.middleware.setup(SQLAlchemySessionMiddleware(SessionLocal))

async def on_shutdown(dp: Dispatcher):
    file_uploader: FileUploader = dp.bot["file_uploader"]
    await file_uploader.close()


async def main(dispatcher):
    import middlewares, filters, handlers
    import logging.config
    from utils.set_bot_command import set_default_commands, set_admin_commands, set_group_commands
    from config import logger_config

    logging.config.dictConfig(logger_config)

    file_uploader = TelegraphService()
    dp.middleware.setup(IntegrationMiddleware(file_uploader))
    bot["file_uploader"] = file_uploader

    # await db.create()
    # await db.create_tables()
    await set_default_commands(dp)
    # await set_admin_commands(dp, chat_id=ADMIN_ID)
    # await set_group_commands(dp, GROUP_ID)

    session = Session()
    await session.get_session()
    bot["session"] = session
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await on_shutdown(dp)
        bot.get("session").close()

if __name__ == '__main__':
    try:
        asyncio.run(main(dp))
    except (KeyboardInterrupt, SystemExit):
        pass

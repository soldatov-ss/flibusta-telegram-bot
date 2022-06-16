from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from utils.database.db_commands import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, timeout=90)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()


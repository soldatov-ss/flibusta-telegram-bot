from aiogram import executor
from loader import dp
import handlers

if __name__ == '__main__':
    executor.start_polling(dp)
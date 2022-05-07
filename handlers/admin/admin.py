import pathlib

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from aiogram.utils.exceptions import BadRequest, TelegramAPIError

from config import CHAT_ID
from loader import dp, db
from utils.throttlig import rate_limit
from aiofile import async_open

@rate_limit(limit=3)
@dp.message_handler(Command('rating_book'))
async def rating(message: types.Message):

    count = await db.select_count_values('books')
    return await message.answer(text=f'Всего было скачано книг: {count}')


@rate_limit(limit=3)
@dp.message_handler(Command('rating_user'))
async def rating(message: types.Message):

    count = await db.select_count_values('users')
    return await message.answer(text=f'Всего в базе пользователей: {count}')


@dp.message_handler(Command('delete'))
async def delete_table(message: types.Message):
    args = message.get_args()
    if args == 'tables' and message.from_user.id == CHAT_ID:
        await db.delete_table_pages()
        await db.create_tables()
    return await message.answer('Таблицы были удалены!')


@dp.message_handler(Command('log_file'))
async def send_log_file(message: types.Message):

    path = pathlib.Path('debug.log').resolve()
    file = InputFile(path)
    try:
        await message.answer_document(file)
        async with async_open(path, 'w') as data:               # Очищаем лог файл, чтобы не было мусора
            await data.write(' ')
    except TelegramAPIError:
        await message.answer('Ошибок пока не было замечено\n'
                             'Лог файл пуст 👌')


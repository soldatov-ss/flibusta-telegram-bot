import pathlib

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from aiogram.utils.exceptions import BadRequest, TelegramAPIError

from config import ADMIN_ID
from loader import dp, db
from utils.throttlig import rate_limit
#from aiofile import async_open

@rate_limit(limit=3)
@dp.message_handler(Command('rating_book'))
async def rating(message: types.Message):

    count, sum_count = await db.select_count_values('books')
    return await message.answer(text=f'Всего было скачано книг: {sum_count}\n'
                                     f'Кол-во уникальных книг: {count}')


@rate_limit(limit=3)
@dp.message_handler(Command('rating_user'))
async def rating(message: types.Message):

    count = await db.select_count_values('users')
    return await message.answer(text=f'Всего в базе пользователей: {count}')



@dp.message_handler(Command('log_file'))
async def send_log_file(message: types.Message):

    path = pathlib.Path('debug.log').resolve()
    file = InputFile(path)
    try:
        await message.answer_document(file)
        with open(path, 'w') as data:               # Очищаем лог файл, чтобы не было мусора
            data.write(' ')
    except TelegramAPIError:
        await message.answer('Ошибок пока не было замечено\n'
                             'Лог файл пуст 👌')


@dp.message_handler(Command('message', prefixes=['!']))
async def message_to_developer(message: types.Message):
    '''
    Сообщение к админу бота
    '''
    text_from_user = ' '.join(message.text.split()[1:])
    if not text_from_user:
        await message.answer('Сообщение не должно быть пустым')
    else:
        await dp.bot.send_message(ADMIN_ID, f'Новое сообщение от {message.from_user.get_mention()}\n\n'
                                  f'<pre>{text_from_user}</pre>')
        await message.reply('Ваше сообщение отправлено!')

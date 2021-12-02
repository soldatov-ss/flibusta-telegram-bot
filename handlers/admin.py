from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db


@dp.message_handler(Command('rating'))
async def rating(message: types.Message):
    args = message.get_args()
    if args:
        if args == 'book':
            count = await db.select_all_books()
            return await message.answer(text=f'Всего было скачано книг: {count}')
        elif args == 'user':
            count = await db.select_all_users()
            return await message.answer(text=f'Всего в базе пользователей: {count}')


@dp.message_handler(Command('delete'))
async def delete_table(message: types.Message):
    args = message.get_args()
    if args == 'tables' and message.from_user.id == '415348636':
        await db.delete_table_pages()
        await db.create_tables()
    return await message.answer('Таблицы были удалены!')

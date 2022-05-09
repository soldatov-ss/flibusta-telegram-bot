import re

from aiogram import types

from keyboards.inline.other_keyboards import get_language, get_formats
from loader import dp, db
from utils.utils import check_link
from utils.parsing.authors import languages
from utils.parsing.books import parsing_formats, description
from utils.parsing.general import get, get_without_register
from utils.throttlig import rate_limit


@rate_limit(limit=3)
@dp.message_handler(regexp=re.compile(r'(^/a_\d+)|(^/a_\d+@)'))
async def chosen_link_author(message: types.Message):
    # Ловим линк и выводим доступные варинаты языков на которых написаны книги
    link = check_link(message.text)
    url = f'http://flibusta.is{link}&lang='

    if message.chat.type == 'private':
        soup = await get_without_register(url)
    else:
        soup = await get(url)

    abbr_lst, languages_lst, author = languages(soup)
    text = f'Книги доступны на следующих языках: \n' \
           f'Ты можешь выбрать удобный для тебя язык 👇'

    await message.answer(text, reply_markup=get_language(
        languages_lst=languages_lst, link=link, abbr_lst=abbr_lst))
    await db.rating_author(author=author, link=link)  # Добавляем автора в базу для рейтинга


@rate_limit(limit=2)
@dp.message_handler(regexp=re.compile(r'(^/b_\d+)|(^/b_\d+@.+)'))
async def chosen_link_book(message: types.Message):
    # Ловим линк и выводим доступные форматы для скачивания
    link = check_link(message.text)  # обрезаем лишнее в ссылке

    book, author, file_formats, descr = await get_book_description(link)
    description = descr[:3*1000].replace('<', '(').replace('>', ')') # Ограничение на длинну текста и убраны скобки, чтобы не падал бот при выводе
    text = f'Автор: <b>{author}</b>\n\n' \
           f'📖 <b>{book}</b>\n\n' \
           f'Описание: \n' \
           f'<i>{description}</i>'

    await message.answer(text=text, reply_markup=get_formats(formats_lst=file_formats, link=link))


async def get_book_description(link):

    url = f'http://flibusta.is{link}'
    data = await db.select_book(link=link)

    if data and data.get('description'):

        descr = data.get('description')
        author = data.get('author')
        book = data.get('book_name')
        formats_list = data.get('formats').split(':')
    else:
        soup = await get(url)
        formats_list = parsing_formats(soup)

        descr, author, book = description(soup)
        formats = ':'.join(formats_list)
        await db.insert_book(book=book, link=link, author=author, formats=formats, description=descr)

    return book, author, formats_list, descr
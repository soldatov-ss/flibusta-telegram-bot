import re

from aiogram import types

from keyboards.inline.other_keyboards import get_language, get_formats
from loader import dp, db
from utils.parsing.authors import languages
from utils.parsing.general import check_chat_type
from utils.parsing.other import get_book_description
from utils.throttlig import rate_limit
from utils.utils import check_link, check_link_from


@rate_limit(limit=3)
@dp.message_handler(regexp=re.compile(r'(^/a_\d+)|(^/a_\d+@)'))
async def chosen_link_author(message: types.Message):
    # Ловим линк и выводим доступные варинаты языков на которых написаны книги
    link = check_link(message.text)
    url = f'http://flibusta.is{link}&lang='

    soup = await check_chat_type(message.chat, url)
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

    link = check_link_from(message)
    book, author, file_formats, descr = await get_book_description(link)

    text = f'Автор: <b>{author}</b>\n\n' \
           f'📖 <b>{book}</b>\n\n' \
           f'Описание: \n' \
           f'<i>{descr}</i>'

    await message.answer(text=text, reply_markup=get_formats(formats_lst=file_formats, link=link))

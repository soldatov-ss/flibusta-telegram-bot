import re

from aiogram import types

from keyboards.inline.formats import get_language, get_formats
from loader import dp, db
from utils.misc import check_link
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

    if message.chat.id == 415348636:  # чат айди бота
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
    url = f'http://flibusta.is{link}'
    soup = await get(url)

    formats_list = parsing_formats(soup)
    descr, author, book = description(soup)
    text = f'Автор: <b>{author}</b>\n\n' \
           f'📖 <b>{book}</b>\n\n' \
           f'Описание: \n' \
           f'<i>{descr}</i>'
    await message.answer(text=text,
                         reply_markup=get_formats(formats_lst=formats_list, link=link))

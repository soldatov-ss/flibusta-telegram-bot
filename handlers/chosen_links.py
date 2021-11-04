import re

from aiogram import types

from keyboards.big_keyboard import get_big_keyboard, big_pagination
from keyboards.formats import get_language, get_formats
from loader import dp, db
from utils.misc import check_link
from utils.pages.generate_pages import create_pages, get_page
from utils.parsing.authors import languages
from utils.parsing.books import parsing_formats, description
from utils.parsing.general import get, get_without_register
from utils.parsing.series import series_books, description_series

CURRENT_BOOKS_LST = []
CURRENT_SERIES_BOOK = ''
series_info = []


@dp.message_handler(regexp=re.compile(r'(^/a_\d+)|(^/a_\d+@)'))
async def chosen_link_author(message: types.Message):
    # Ловим линк и выводим доступные варинаты языков на которых написаны книги
    link = check_link(message.text)
    url = f'http://flibusta.is{link}&lang='

    soup = await get(url)
    abbr_lst, languages_lst, author = languages(soup)
    text = f'Книги доступны на следующих языках: \n' \
           f'Ты можешь выбрать удобный для тебя язык 👇'

    await message.answer(text, reply_markup=get_language(
        languages_lst=languages_lst, link=link, abbr_lst=abbr_lst))
    await db.add_author(author=author, link=link)  # Добавляем автора в базу для рейтинга


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


@dp.message_handler(regexp=re.compile(r'(^/sequence_\d+)|(^/sequence_\d+@)'))
async def chosen_link_series(message: types.Message):
    # Все книги серии
    global CURRENT_BOOKS_LST, CURRENT_SERIES_BOOK, series_info
    link = check_link(message.text)
    url = f'http://flibusta.is{link}?pages='
    soup = await get(url)

    series_books_dict = await series_books(link)  # Все книги выбранной серии
    series_name, series_author, series_genres = description_series(soup)  # Описание серии
    count_books = len(series_books_dict.keys())

    series_info = [series_name, series_author, series_genres]
    CURRENT_SERIES_BOOK = link
    CURRENT_BOOKS_LST = create_pages(
        series_books_dict, count_items=count_books, flag='series_books')

    current_page_text = get_page(
        items_list=CURRENT_BOOKS_LST, series_lst=[series_name, series_author, series_genres])

    await message.answer(
        current_page_text,
        reply_markup=get_big_keyboard(count_pages=len(CURRENT_BOOKS_LST), key=CURRENT_SERIES_BOOK,
                                      method='series_books'))


@dp.callback_query_handler(big_pagination.filter(page='current_page'))
async def current_page_error(call: types.CallbackQuery):
    # убираем часики по нажанию на текущую страницу
    return await call.answer(cache_time=60)


# Пагинация при показе всех доступных книг выбранной серии
@dp.callback_query_handler(big_pagination.filter())
async def characters_page_callback(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_SERIES_BOOK:
        # Отменяем пагинацию в прошлом сообщении
        return await call.answer(cache_time=60)

    current_page = int(callback_data['page'])
    current_page_text = get_page(
        items_list=CURRENT_BOOKS_LST, page=current_page, series_lst=series_info)

    await call.message.edit_text(text=current_page_text,
                                 reply_markup=get_big_keyboard(count_pages=len(CURRENT_BOOKS_LST),
                                                               key=CURRENT_SERIES_BOOK, page=current_page,
                                                               method='series_books'))

import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import MessageNotModified

from utils.utils import check_link, create_current_name

from keyboards.inline.big_keyboard import big_pagination, get_big_keyboard
from keyboards.inline.small_keyboard import get_small_keyboard, pagination_call
from loader import dp, db
from utils.pages.generate_list_pages import get_list_pages, get_series_pages, get_from_request_pages, \
    get_from_request_series_pages
from utils.pages.generate_pages import get_page
from utils.parsing.series import search_series
from utils.throttlig import rate_limit
from utils.utils import get_message_text


@rate_limit(limit=4)
@dp.message_handler(Command('series'))
async def series_command(message: types.Message):
    # Все доступные книжные серии
    series_name = await get_message_text(message, method='series')
    if not series_name: return
    url = f'http://flibusta.is/booksearch?ask={series_name}&chs=on'

    current_series_hash = create_current_name(message.chat.type, series_name.title())
    series_pages, data_from_db = await get_list_pages(current_series_hash, message.chat, url, method='series',
                                                      func=search_series)
    if series_pages:
        current_page = get_page(series_pages)

        await message.answer(current_page, reply_markup=get_small_keyboard(
            count_pages=len(series_pages), key=current_series_hash, method='series'))

        if data_from_db:
            updated_list_pages = await get_from_request_pages(message.chat, func=search_series, method='series',
                                                              url=url)
            await db.update_book_pages(current_series_hash, updated_list_pages, table_name='series_pages')


@rate_limit(limit=3)
@dp.message_handler(regexp=re.compile(r'(^/sequence_\d+)|(^/sequence_\d+@)'))
async def chosen_link_series(message: types.Message):
    # Все книги выбранной книжной серии
    link = check_link(message.text)
    url = f'http://flibusta.is{link}?pages='

    current_series_link_hash = create_current_name(message.chat.type, link, flag=True)

    book_pages = await get_series_pages(current_series_link_hash, message.chat, url, link)
    if book_pages:
        series_pages, series_info, data_from_db = book_pages
        current_page_text = get_page(items_list=series_pages, series_lst=series_info)

        await message.answer(current_page_text, reply_markup=get_big_keyboard(
            count_pages=len(series_pages), key=current_series_link_hash, method='series_books'))

        if data_from_db:  # Обновляем в БД данные по доступным книгам
            updated_list_pages, series_info = await get_from_request_series_pages(message.chat, url, link)
            await db.update_book_pages(current_series_link_hash, updated_list_pages,
                                       table_name='series_book_pages', column='pages')


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='series'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    current_series_name, series_books_pages = await db.select_pages(callback_data['key'], table_name='series_pages')
    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=series_books_pages, page=current_page)

    markup = get_small_keyboard(
        count_pages=len(series_books_pages), key=current_series_name, page=current_page, method='series')
    try:
        await call.message.edit_text(current_page_text, reply_markup=markup)
    except MessageNotModified:
        pass
    await call.answer()


# Пагинация при показе всех доступных книг выбранной серии
@dp.callback_query_handler(big_pagination.filter())
async def characters_page_callback(call: types.CallbackQuery, callback_data: dict):
    current_series_name, series_pages, series_info = await db.select_pages(
        callback_data['key'], 'series_book_pages', 'series_name', 'series_author', 'series_genres', 'pages')

    current_page = int(callback_data['page'])
    current_page_text = get_page(
        items_list=series_pages, page=current_page, series_lst=series_info)
    try:
        await call.message.edit_text(text=current_page_text, reply_markup=get_big_keyboard(
            count_pages=len(series_pages), key=current_series_name, page=current_page, method='series_books'))
    except MessageNotModified:
        pass
    await call.answer()

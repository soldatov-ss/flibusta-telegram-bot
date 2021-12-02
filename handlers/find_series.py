import hashlib
import re

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.big_keyboard import big_pagination, get_big_keyboard
from keyboards.inline.small_keyboard import get_small_keyboard, pagination_call
from loader import dp, db
from utils.check_args import check_args
from utils.misc import check_link, check_group_or_bot_for_series_books, \
    check_group_or_bot
from utils.pages.generate_pages import create_pages, get_page
from utils.parsing.series import description_series, search_series
from utils.throttlig import rate_limit


@rate_limit(limit=4)
@dp.message_handler(Command('series'))
async def series_command(message: types.Message):
    # Все доступные книжные серии
    series_name = message.get_args()

    text = check_args(series_name, 'series')  # Проверяем не пусты ли аргументы на команду /series
    if text: return await message.answer(text)

    url = f'https://flibusta.is/booksearch?ask={series_name}&chs=on'

    series_info = await check_group_or_bot(message.chat.id, url, func=search_series, method='series')
    if series_info:
        series_dict, count_series, group_or_bot = series_info
        series_pages = create_pages(books_dict=series_dict, count_items=count_series, flag='series')

        current_series_name = hashlib.md5((series_name + group_or_bot).encode()).hexdigest()
        current_page = get_page(series_pages)

        await message.answer(current_page,
                             reply_markup=get_small_keyboard(
                                 count_pages=len(series_pages), key=current_series_name, method='series'))
        await db.add_new_pages(series_pages, current_series_name)


@dp.message_handler(regexp=re.compile(r'(^/sequence_\d+)|(^/sequence_\d+@)'))
async def chosen_link_series(message: types.Message):
    # Все книги выбранной книжной серии
    link = check_link(message.text)
    url = f'http://flibusta.is{link}?pages='

    series_books_info = await check_group_or_bot_for_series_books(message.chat.id, url, link)
    if series_books_info:
        series_book_dict, count_books, group_or_bot, soup = series_books_info

        series_name, series_author, series_genres = description_series(soup)  # Описание серии
        series_info = [series_name, series_author, series_genres]

        current_series_link = group_or_bot + link
        series_pages = create_pages(series_book_dict, count_items=count_books, flag='series_books')
        current_page_text = get_page(items_list=series_pages, series_lst=series_info)

        await message.answer(
            current_page_text,
            reply_markup=get_big_keyboard(count_pages=len(series_pages), key=current_series_link,
                                          method='series_books'))
        await db.add_new_series_pages(series_pages, current_series_link, series_name, series_author, series_genres)


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='series'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с авторами, чтобы пагинация просто отключалась
        current_series_name, series_books_pages = await db.find_pages(callback_data['key'])
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=series_books_pages, page=current_page)

    markup = get_small_keyboard(
        count_pages=len(series_books_pages), key=current_series_name, page=current_page, method='series')

    await call.message.edit_text(current_page_text, reply_markup=markup)
    await call.answer()


# Пагинация при показе всех доступных книг выбранной серии
@dp.callback_query_handler(big_pagination.filter())
async def characters_page_callback(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с авторами, чтобы пагинация просто отключалась
        current_series_name, series_pages, series_info = await db.series_pages(callback_data['key'])
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data['page'])
    current_page_text = get_page(
        items_list=series_pages, page=current_page, series_lst=series_info)

    await call.message.edit_text(text=current_page_text,
                                 reply_markup=get_big_keyboard(count_pages=len(series_pages),
                                                               key=current_series_name, page=current_page,
                                                               method='series_books'))

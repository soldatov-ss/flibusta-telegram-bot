from aiogram import types
from utils.restrictions import CheckFromUser

from loader import db
from utils.pages.generate_pages import create_pages
from utils.parsing.authors import author_books
from utils.parsing.series import description_series, series_books


async def get_from_request_pages(chat: types.Chat, func, method: str, url: str):
    request_info = await CheckFromUser(chat, url, function=func, method=method).check_chat_type()
    if not request_info: return

    res_dict, count_items = request_info
    list_pages = create_pages(res_dict, count_items, method)
    return list_pages


async def get_from_request_author_pages(chat: types.Chat, url: str):

    request_info = await CheckFromUser(
        chat, url, function=author_books, method='book').check_chat_type()

    if not request_info: return
    book_dict, count_books, author_name = request_info

    list_pages = create_pages(book_dict, count_items=count_books, flag='author_books')
    return list_pages, count_books, author_name


async def get_from_request_series_pages(chat: types.Chat, url: str, link: str):

    request_info = await CheckFromUser(
        chat, url, function=series_books, method='book').result_for_series_book(link)
    if not request_info: return

    book_dict, count_books, soup = request_info
    list_pages = create_pages(book_dict, count_items=count_books, flag='series_books')

    series_name, series_author, series_genres = description_series(soup)  # Описание серии
    series_info = [series_name, series_author, series_genres]
    return list_pages, series_info


async def get_list_pages(current_name, chat: types.Chat, url: str, method: str, func):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД
    data_from_db = False
    pages = await db.select_pages(current_name, f'{method}_pages')

    if pages:
        list_pages = pages[1]
        data_from_db = True
    else:
        list_pages = await get_from_request_pages(chat, func, method, url)
        if list_pages: await db.add_new_pages(f'{method}_pages', list_pages, current_name)

    return list_pages, data_from_db


async def get_author_pages(current_book_hash, chat: types.Chat, url: str):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД
    data_from_db = False

    pages = await db.select_pages(current_book_hash, 'author_book_pages', 'author_name', 'pages', 'сount_books')
    if pages:
        _, list_pages, author_name, count_books = pages
        data_from_db = True
    else:
        pages = await get_from_request_author_pages(chat, url)
        if not pages: return

        list_pages, count_books, author_name = pages
        await db.add_new_author_book_pages(list_pages, current_book_hash, count_books, author_name)

    return list_pages, author_name, count_books, data_from_db


async def get_series_pages(current_name_hash, chat: types.Chat, url: str, link: str):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД

    data_from_db = False

    pages = await db.select_pages(current_name_hash, 'series_book_pages', 'series_name', 'series_author', 'series_genres', 'pages')
    if pages:
        _, list_pages, series_info = pages
        data_from_db = True
    else:
        pages = await get_from_request_series_pages(chat, url, link)
        if not pages: return

        list_pages, series_info = pages
        series_name, series_author, series_genres = series_info
        await db.add_new_series_book_pages(list_pages, current_name_hash, series_name, series_author, series_genres)

    return list_pages, series_info, data_from_db

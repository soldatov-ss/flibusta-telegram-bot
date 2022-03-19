from loader import db
from utils.misc import check_group_or_bot, check_group_or_bot_for_author_books, check_group_or_bot_for_series_books
from utils.pages.generate_pages import create_pages
from utils.parsing.series import description_series


async def get_from_request_pages(chat_id: int, func, method: str, url: str):
    request_info = await check_group_or_bot(chat_id, url, func=func, method=method)
    if not request_info: return
    res_dict, count_items, _ = request_info
    list_pages = create_pages(res_dict, count_items, method)
    return list_pages


async def get_from_request_author_pages(chat_id: int, url: str):
    request_info = await check_group_or_bot_for_author_books(chat_id, url)
    if not request_info: return
    book_dict, count_books, _, author_name = request_info

    list_pages = create_pages(book_dict, count_items=count_books, flag='author_books')
    return list_pages, count_books, author_name


async def get_from_request_series_pages(chat_id: int, url: str, link: str):
    request_info = await check_group_or_bot_for_series_books(chat_id, url, link)
    if not request_info: return

    book_dict, count_books, _, soup = request_info
    list_pages = create_pages(book_dict, count_items=count_books, flag='series_books')

    series_name, series_author, series_genres = description_series(soup)  # Описание серии
    series_info = [series_name, series_author, series_genres]
    return list_pages, series_info


async def get_list_pages(current_name, chat_id: int, url: str, method: str, func):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД
    flag = False
    pages = await db.find_pages(current_name, f'{method}_pages')

    if pages:
        list_pages = pages[1]
        flag = True
    else:
        list_pages = await get_from_request_pages(chat_id, func, method, url)
        if list_pages: await db.add_new_pages(f'{method}_pages', list_pages, current_name)

    return list_pages, flag


async def get_author_pages(current_book_hash, chat_id: int, url: str):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД
    flag = False
    pages = await db.author_pages(current_book_hash)
    if pages:
        _, list_pages, author_name, count_books = pages
        flag = True
    else:
        pages = await get_from_request_author_pages(chat_id, url)
        if not pages: return

        list_pages, count_books, author_name = pages
        await db.add_new_author_book_pages(list_pages, current_book_hash, count_books, author_name)

    return list_pages, author_name, count_books, flag


async def get_series_pages(current_name_hash, chat_id: int, url: str, link: str):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД

    flag = False
    pages = await db.series_pages(current_name_hash)
    if pages:
        _, list_pages, series_info = pages
        flag = True
    else:
        pages = get_from_request_series_pages(chat_id, url, link)
        if not pages: return

        list_pages, series_info = pages
        series_name, series_author, series_genres = series_info
        await db.add_new_series_book_pages(list_pages, current_name_hash, series_name, series_author, series_genres)

    return list_pages, series_info, flag

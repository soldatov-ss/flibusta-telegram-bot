import hashlib

from loader import bot, db
from utils.pages.generate_pages import create_pages
from utils.pages.strings import strings_for_user_into_bot
from utils.parsing.authors import author_books, search_authors
from utils.parsing.general import get, get_without_register
from utils.parsing.series import series_books, description_series


def check_link(link: str):
    # /b_101112@my_flibusta_bot
    link = link.replace('_', '/')
    if '@' in link:
        link = link[:link.find('@')]
    # /b/101112
    return link


def create_current_name(chat_id: int, name: str, flag=False):
    # Проверка, откуда запрос, с бота или с группы ибо есть ограничения в боте, в группе же нету
    # Хешируем, чтобы обойти ограничение в 64 байта для CallbackData

    if chat_id == 415348636:
        current_item = 'bot' + name
    else:
        current_item = 'group' + name
    if not flag:  # Только для авторов и книг с серии
        current_item_hash = hashlib.md5(current_item.encode()).hexdigest()
    else:
        current_item_hash = current_item
    return current_item_hash


async def get_list_pages(current_name, chat_id: int, url: str, method: str):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД

    pages = await db.find_pages(current_name, f'{method}_pages')
    if pages:
        list_pages = pages[1]
    else:
        request_info = await check_group_or_bot(chat_id, url, func=search_authors, method=method)

        if not request_info: return
        res_dict, count_items, _ = request_info
        list_pages = create_pages(res_dict, count_items, method)

        await db.add_new_pages(f'{method}_pages', list_pages, current_name)

    return list_pages


async def get_author_pages(current_book_hash, chat_id: int, url: str):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД

    pages = await db.author_pages(current_book_hash)
    if pages:
        _, list_pages, author_name, count_books = pages
    else:
        request_info = await check_group_or_bot_for_author_books(chat_id, url)
        if not request_info: return
        book_dict, count_books, _, author_name = request_info

        list_pages = create_pages(book_dict, count_items=count_books, flag='author_books')
        await db.add_new_author_book_pages(list_pages, current_book_hash, count_books, author_name)

    return list_pages, author_name, count_books


async def get_series_pages(current_name_hash, chat_id: int, url: str, link):
    # Получаем список с результатом, если есть в БД - выводим
    # Если нету в БД - парсим и добавляем в БД

    pages = await db.series_pages(current_name_hash)
    if pages:
        _, list_pages, series_info = pages
    else:
        request_info = await check_group_or_bot_for_series_books(chat_id, url, link)
        if not request_info: return
        book_dict, count_books, _, soup = request_info

        list_pages = create_pages(book_dict, count_items=count_books, flag='series_books')

        series_name, series_author, series_genres = description_series(soup)  # Описание серии
        series_info = [series_name, series_author, series_genres]

        await db.add_new_series_book_pages(list_pages, current_name_hash, series_name, series_author, series_genres)

    return list_pages, series_info


async def check_group_or_bot(chat_id: int, url: str, func, method: str):
    soup_with = await get(url)
    if chat_id == 415348636:  # чат айди, если запрос пришел с бота, а не с группы
        soup_without = await get_without_register(url)

        if not func(soup_with):
            text = strings_for_user_into_bot(no_result_message=method)
            await bot.send_message(chat_id, text)
            return False

        elif not func(soup_without) and func(soup_with):
            text = strings_for_user_into_bot(danger_message=True)
            await bot.send_message(chat_id, text)
            return False

        elif func(soup_without):
            text = strings_for_user_into_bot(second_message=method)
            await bot.send_message(chat_id, text)

            book_dict_without, count_books_without = func(soup_without)
            return book_dict_without, count_books_without, 'bot'

    else:
        if not func(soup_with):
            text = strings_for_user_into_bot(no_result_message=method)
            await bot.send_message(chat_id, text)
            return False

        else:
            book_dict_with, count_books_with = func(soup_with)
            return book_dict_with, count_books_with, 'group'


async def check_group_or_bot_for_author_books(chat_id, url):
    soup_with = await get(url)
    if chat_id != 415348636:
        soup_without = await get_without_register(url)

        if not author_books(soup_without) and author_books(soup_with):
            text = strings_for_user_into_bot(danger_message=True)
            await bot.send_message(chat_id, text)
            return False

        elif author_books(soup_without):
            text = strings_for_user_into_bot(second_message='book')
            await bot.send_message(chat_id, text)

            book_dict_without, count_books_without, author = author_books(soup_without)
            return book_dict_without, count_books_without, 'bot', author

    else:
        book_dict_with, count_books_with, author = author_books(soup_with)
        return book_dict_with, count_books_with, 'group', author


async def check_group_or_bot_for_series_books(chat_id, url, link):
    soup_with = await get(url)

    if chat_id == 415348636:
        text = strings_for_user_into_bot(second_message='books')
        await bot.send_message(chat_id, text)
        series_book_dict, count_series_books = await series_books(soup_with, link)
        return series_book_dict, count_series_books, 'bot', soup_with

    else:
        series_book_dict_with, count_series_books_with = await series_books(soup_with, link)
        return series_book_dict_with, count_series_books_with, 'group', soup_with

# ??? Сделать позже новый парсер? ибо на этом без регистрации нет результата
# async def check_group_or_bot_for_series_books(chat_id, url, link):
#     soup_with = await get(url)
#
#     if str(chat_id) == '415348636':
#         soup_without = await get_without_register(url)
#
#         if not await series_books(soup_without, link) and await series_books(soup_with, link):
#             text = strings_for_user_into_bot(danger_message=True)
#             await bot.send_message(chat_id, text)
#             return False
#         else:
#             text = strings_for_user_into_bot(second_message='books')
#             await bot.send_message(chat_id, text)
#
#             series_book_dict_without, count_series_books_without = await series_books(soup_without, link)
#             return series_book_dict_without, count_series_books_without, 'bot', soup_with
#
#     else:
#         series_book_dict_with, count_series_books_with = await series_books(soup_with, link)
#         return series_book_dict_with, count_series_books_with, 'group', soup_with

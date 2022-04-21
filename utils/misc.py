import hashlib

from aiogram import types

from loader import bot
from utils.pages.strings import strings_for_user_into_bot
from utils.parsing.authors import author_books
from utils.parsing.general import get, get_without_register
from utils.parsing.series import series_books


def check_link(link: str):
    # /b_101112@my_flibusta_bot
    link = link.replace('_', '/')
    if '@' in link:
        link = link[:link.find('@')]
    # /b/101112
    return link


def create_current_name(chat_type: str, name: str, flag=False):
    # Проверка, откуда запрос, с бота или с группы ибо есть ограничения в боте, в группе же нету
    # Хешируем, чтобы обойти ограничение в 64 байта для CallbackData

    if chat_type == 'private':
        current_item = 'bot' + name
    else:
        current_item = 'group' + name
    if not flag:  # Только для авторов и книг с серии
        current_item_hash = hashlib.md5(current_item.encode()).hexdigest()
    else:
        current_item_hash = current_item
    return current_item_hash


async def check_group_or_bot(chat: types.Chat, url: str, func, method: str):
    soup_with = await get(url)
    if chat.type == 'private':  # чат айди, если запрос пришел с бота, а не с группы
        soup_without = await get_without_register(url)
        if not func(soup_with):
            text = strings_for_user_into_bot(no_result_message=method)
            await bot.send_message(chat.id, text)
            return False

        elif not func(soup_without) and func(soup_with):
            text = strings_for_user_into_bot(danger_message=True)
            await bot.send_message(chat.id, text)
            return False

        elif func(soup_without):
            text = strings_for_user_into_bot(second_message=method)
            await bot.send_message(chat.id, text)

            book_dict_without, count_books_without = func(soup_without)
            return book_dict_without, count_books_without, 'bot'
    else:
        if not func(soup_with):
            text = strings_for_user_into_bot(no_result_message=method)
            await bot.send_message(chat.id, text)
            return False

        else:
            book_dict_with, count_books_with = func(soup_with)
            return book_dict_with, count_books_with, 'group'

async def check_group_or_bot_for_author_books(chat: types.Chat, url):
    soup_with = await get(url)
    if chat.type == 'private':
        soup_without = await get_without_register(url)
        if not author_books(soup_without) and author_books(soup_with):
            text = strings_for_user_into_bot(danger_message=True)
            await bot.send_message(chat.id, text)
            return False

        elif author_books(soup_without):
            text = strings_for_user_into_bot(second_message='book')
            await bot.send_message(chat.id, text)

            book_dict_without, count_books_without, author = author_books(soup_without)
            return book_dict_without, count_books_without, 'bot', author


    else:
        book_dict_with, count_books_with, author = author_books(soup_with)
        return book_dict_with, count_books_with, 'group', author


async def check_group_or_bot_for_series_books(chat: types.Chat, url, link):
    soup_with = await get(url)

    if chat.type == 'private':
        text = strings_for_user_into_bot(second_message='book')
        await bot.send_message(chat.id, text)
        series_book_dict, count_series_books = await series_books(soup_with, link)
        return series_book_dict, count_series_books, 'bot', soup_with

    else:
        series_book_dict_with, count_series_books_with = await series_books(soup_with, link)
        return series_book_dict_with, count_series_books_with, 'group', soup_with

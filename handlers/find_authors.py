import hashlib
import json

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.big_keyboard import get_big_keyboard, big_pagination
from keyboards.inline.formats import languages_call
from keyboards.inline.small_keyboard import get_small_keyboard, pagination_call
from loader import dp, db
from utils.check_args import check_args
from utils.misc import check_group_or_bot_for_author_books, check_group_or_bot
from utils.pages.generate_pages import create_pages, get_page
from utils.parsing.authors import search_authors
from utils.throttlig import rate_limit


@rate_limit(limit=3)
@dp.message_handler(Command('author'))
async def author_command(message: types.Message):
    author = message.get_args()
    text = check_args(author, 'author')  # Проверяем не пусты ли аргументы на команду /author
    if text: return await message.answer(text)

    url = f'http://flibusta.is//booksearch?ask={author}&cha=on'
    authors_info = await check_group_or_bot(message.chat.id, url, func=search_authors, method='authors')

    if authors_info:
        authors_dict, count_authors, group_or_bot = authors_info
        authors_pages = create_pages(authors_dict, count_authors, 'authors')  # Общий список книг

        current_author = group_or_bot + author.title()
        current_author_hash = hashlib.md5(
            current_author.encode()).hexdigest()
        current_page_text = get_page(items_list=authors_pages)

        await message.answer(current_page_text,
                             reply_markup=get_small_keyboard(
                                 count_pages=len(authors_pages), key=current_author_hash, method='author'))
        await db.add_new_pages(authors_pages, current_author_hash)


@dp.callback_query_handler(languages_call.filter())
async def current_languages(call: types.CallbackQuery, callback_data: dict):
    # Вывод список доступных книг по выбранному языку
    language = callback_data['abbr']
    link = callback_data['link']
    chat_id = json.loads(call.as_json()).get('message').get('chat')['id']

    url = f'http://flibusta.is{link}&lang={language}&order=p&hg1=1&hg=1&sa1=1&hr1=1'
    author_books_info = await check_group_or_bot_for_author_books(chat_id, url)

    if author_books_info:
        author_books_dict, count_author_books, group_or_bot, author_name = author_books_info
        author_books_pages = create_pages(author_books_dict, count_items=count_author_books, flag='author_books')

        current_author_link = group_or_bot + link + language
        current_page = get_page(author_books_pages, author=[author_name, count_author_books])
        await call.message.answer(current_page,
                                  reply_markup=get_big_keyboard(count_pages=len(author_books_pages),
                                                                key=current_author_link, method='author_books'))
        await db.add_new_author_pages(author_books_pages, current_author_link, count_author_books, author_name)
        await call.answer()


# Пагинация при показе всех доступных авторов
@dp.callback_query_handler(pagination_call.filter(method='author'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с авторами, чтобы пагинация просто отключалась
        current_author, authors_lst = await db.find_pages(callback_data['key'])
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=authors_lst, page=current_page)

    markup = get_small_keyboard(count_pages=len(authors_lst), key=current_author, page=current_page, method='author')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)
    await call.answer()


# Пагинация при показе всех доступных книг автора
@dp.callback_query_handler(big_pagination.filter(method='author_books'))
async def show_chosen(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с книгами, чтобы пагинация просто отключалась
        current_author_link, author_books_lst, author_name, count_books = await db.author_pages(callback_data['key'])
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(
        items_list=author_books_lst, author=[author_name, count_books], page=current_page)

    markup = get_big_keyboard(count_pages=len(author_books_lst), key=current_author_link,
                              page=current_page, method='author_books')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)
    await call.answer()

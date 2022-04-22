from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContextProxy

from keyboards.inline.big_keyboard import get_big_keyboard, big_pagination
from keyboards.inline.formats import languages_call
from keyboards.inline.small_keyboard import get_small_keyboard, pagination_call
from loader import dp, db
from utils.misc import create_current_name
from utils.pages.generate_list_pages import get_list_pages, get_author_pages, get_from_request_pages, \
    get_from_request_author_pages
from utils.pages.generate_pages import get_page
from utils.parsing.authors import search_authors
from utils.throttlig import rate_limit
from utils.utils import get_message_text


@rate_limit(limit=3)
@dp.message_handler(Command('author'))
async def author_command(message: types.Message | FSMContextProxy):
    author =  await get_message_text(message, method='author')
    if not author: return

    url = f'http://flibusta.is//booksearch?ask={author}&cha=on'

    current_author_hash = create_current_name(message.chat.type, author.title())
    authors_pages, flag = await get_list_pages(current_author_hash, message.chat, url, method='author',
                                               func=search_authors)

    if authors_pages:
        current_page_text = get_page(items_list=authors_pages)

        await message.answer(current_page_text, reply_markup=get_small_keyboard(
            count_pages=len(authors_pages), key=current_author_hash, method='author'))

        if flag: # Обновляем в БД данные по доступным авторам
            updated_list_pages = await get_from_request_pages(message.chat, func=search_authors, method='author', url=url)
            await db.update_book_pages(current_author_hash, updated_list_pages, table_name='author_pages')


@dp.callback_query_handler(languages_call.filter())
async def current_languages(call: types.CallbackQuery, callback_data: dict):
    # Вывод списока доступных книг по выбранному языку

    language = callback_data['abbr']
    link = callback_data['link']

    url = f'http://flibusta.is{link}&lang={language}&order=p&hg1=1&hg=1&sa1=1&hr1=1'

    current_author_link = create_current_name(call.message.chat.type, link + language, flag=True)
    book_pages = await get_author_pages(current_author_link, call.message.chat, url)

    if book_pages:
        book_pages, author_name, count_books, flag = book_pages

        current_page = get_page(book_pages, author=[author_name, count_books])
        await call.message.answer(current_page,
                                  reply_markup=get_big_keyboard(count_pages=len(book_pages),
                                                                key=current_author_link, method='author_books'))
        await call.answer()

        if flag: # Обновляем в БД данные по доступным книгам
            updated_list_pages, count_books, _ = await get_from_request_author_pages(call.message.chat, url=url)
            await db.update_author_pages(updated_list_pages, current_author_link, count_books)



# Пагинация при показе всех доступных авторов
@dp.callback_query_handler(pagination_call.filter(method='author'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с авторами, чтобы пагинация просто отключалась
        current_author, authors_lst = await db.select_pages(callback_data['key'], table_name='author_pages')
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
        current_author_link, author_books_lst, author_name, count_books = await db.select_pages(
            callback_data['key'], 'author_book_pages', 'author_name', 'pages', 'сount_books')
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(
        items_list=author_books_lst, author=[author_name, count_books], page=current_page)

    markup = get_big_keyboard(count_pages=len(author_books_lst), key=current_author_link,
                              page=current_page, method='author_books')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)
    await call.answer()

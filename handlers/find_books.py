from aiogram import types

from keyboards.inline.small_keyboard import get_small_keyboard, pagination_call
from loader import dp, db
from utils.check_args import check_args
from utils.misc import create_current_name
from utils.pages.generate_list_pages import get_list_pages, get_from_request_pages
from utils.pages.generate_pages import get_page
from utils.parsing.books import search_books


@dp.message_handler()
async def find_books(message: types.Message):
    text = check_args(message.text, 'book')  # Проверяем на длину запроса, чтобы не был слишком краток
    if text: return await message.answer(text)
    url = f'http://flibusta.is//booksearch?ask={message.text}&chb=on'

    current_book_hash = create_current_name(message.chat.id, message.text.title())
    books_pages, flag = await get_list_pages(current_book_hash, message.chat.id, url, method='book', func=search_books)

    if books_pages:
        current_page_text = get_page(items_list=books_pages)

        await message.answer(current_page_text, reply_markup=get_small_keyboard(
            count_pages=len(books_pages), key=current_book_hash, method='book'))

        if flag: # Обновляем в БД данные по доступным книгам
            updated_list_pages = await get_from_request_pages(message.chat.id, func=search_books, method='book', url=url)
            await db.update_book_pages(current_book_hash, updated_list_pages, table_name='book_pages')


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='book'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с книгами, чтобы пагинация просто отключалась
        current_book, books_lst = await db.find_pages(callback_data['key'], table_name='book_pages')
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=books_lst, page=current_page)

    markup = get_small_keyboard(count_pages=len(books_lst), key=current_book, page=current_page, method='book')
    await call.message.edit_text(current_page_text, reply_markup=markup)
    await call.answer()

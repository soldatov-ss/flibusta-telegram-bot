import hashlib

from aiogram import types

from keyboards.small_keyboard import get_small_keyboard, pagination_call
from loader import dp, db
from utils.check_args import check_args
from utils.misc import check_group_or_bot
from utils.pages.generate_pages import create_pages, get_page


@dp.message_handler()
async def find_books(message: types.Message):
    # Эхо хендлер по названию книги, обрабатывает всё и показывает первую страницу списка
    text = check_args(message.text, 'book')  # Проверяем не пусты ли аргументы на команду /book
    if text: return await message.answer(text)
    url = f'http://flibusta.is//booksearch?ask={message.text}&chb=on'

    books_info = await check_group_or_bot(message.chat.id, url)
    if books_info:
        books_dict, count_books, group_or_bot = books_info
        books_pages = create_pages(books_dict, count_books, 'books')  # Общий список книг

        current_book = group_or_bot + message.text.title()
        current_book_hash = hashlib.md5(
            current_book.encode()).hexdigest()  # Хешируем, чтобы обойти ограничение в 64 байта для CallbackData

        current_page_text = get_page(items_list=books_pages)

        await message.answer(current_page_text,
                             reply_markup=get_small_keyboard(
                                 count_pages=len(books_pages), key=current_book_hash, method='book'))
        await db.add_new_pages(books_pages, current_book_hash)


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='book'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    try:
        # На случай если в базе не будет списка с книгами, чтобы пагинация просто отключалась
        current_book, books_lst = await db.find_pages(callback_data['key'])
    except TypeError:
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=books_lst, page=current_page)

    markup = get_small_keyboard(count_pages=len(books_lst), key=current_book, page=current_page, method='book')
    await call.message.edit_text(current_page_text, reply_markup=markup)
    await call.answer()

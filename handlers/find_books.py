import hashlib

from aiogram import types

from keyboards.small_keyboard import get_small_keyboard, pagination_call
from loader import dp
from utils.check_args import check_args
from utils.pages.generate_pages import create_pages, get_page
from utils.parsing.books import search_books
from utils.parsing.general import get

BOOKS_LST = []
CURRENT_BOOK = ''


@dp.message_handler()
async def find_books(message: types.Message):
    # Эхо хендлер по названию книги, обрабатывает всё и показывает первую страницу списка
    global BOOKS_LST, CURRENT_BOOK

    text = check_args(message.text, 'book')  # Проверяем не пусты ли аргументы на команду /book
    if text: return await message.answer(text)

    url = f'http://flibusta.is//booksearch?ask={message.text}&chb=on'
    # url = f'http://flibustahezeous3.onion/booksearch?ask={message.text}&chb=on'
    soup = await get(url)

    if not search_books(soup):
        return await message.reply(text='По запросу ничего не найдено! 😔\n' \
                                        'Введи название книги для поиска 😌')

    parse_dict, count_books = search_books(soup)  # Возвращаем словарь и кол-во найденных книг

    CURRENT_BOOK = hashlib.md5(
        message.text.encode()).hexdigest()  # Хешируем, чтобы обойти ограничение в 64 байта для CallbackData
    BOOKS_LST = create_pages(parse_dict, count_books, 'books')  # Общий список книг

    current_page = get_page(items_list=BOOKS_LST)
    await message.answer(current_page,
                         reply_markup=get_small_keyboard(
                             count_pages=len(BOOKS_LST), key=CURRENT_BOOK, method='book'))


@dp.callback_query_handler(pagination_call.filter(page='current_page'))
async def current_page_error(call: types.CallbackQuery):
    # убираем часики по нажанию на текущую страницу
    await call.answer(cache_time=60)


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='book'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_BOOK:
        # Блокировка в предыдущем сообщении паганиции
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('pages'))
    current_page_text = get_page(items_list=BOOKS_LST, page=current_page)

    markup = get_small_keyboard(count_pages=len(BOOKS_LST), key=CURRENT_BOOK, page=current_page, method='book')
    await call.message.edit_text(current_page_text, reply_markup=markup)

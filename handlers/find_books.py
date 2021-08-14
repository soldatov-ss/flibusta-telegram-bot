import hashlib
import re

from aiogram import types

from keyboards.formats import get_formats
from keyboards.pagination import get_page_keyboard, pagination_call
from loader import dp
from utils.pages import create_pages, get_page
from utils.parsing.books import search_books, parsing_formats, description
from utils.parsing.general import get

list_books = []
CURRENT_BOOK = ''


@dp.message_handler(regexp=re.compile(r'^/b_\d+'))
async def chosen_link(message: types.Message):
    # Ловим линк и выводим доступные форматы для скачивания
    link = message.text.replace('_', '/')
    url = f'http://flibusta.is{link}'
    # url = f'http://flibustahezeous3.onion{link}'
    soup = await get(url)
    formats_list = parsing_formats(soup)
    descr, author, book = description(soup)

    text = f'Автор: <b>{author}</b>\n\n' \
           f'📖 <b>{book}</b>\n\n' \
           f'Описание: \n' \
           f'<i>{descr}</i>'
    await message.answer(text=text,
                         reply_markup=get_formats(formats_lst=formats_list, link=link))


@dp.message_handler()
async def find_books(message: types.Message):
    # Эхо хендлер по названию книги, обрабатывает всё и показывает первую страницу списка
    global list_books, CURRENT_BOOK
    if len(message.text) <= 2:
        return await message.reply('⛔️Слишком короткое название, попробуй еще раз')

    url = f'http://flibusta.is//booksearch?ask={message.text}&chb=on'
    # url = f'http://flibustahezeous3.onion/booksearch?ask={message.text}&chb=on'
    soup = await get(url)

    if not search_books(soup):
        return await message.reply(text='По запросу ничего не найдено! 😔\n' \
                                        'Введи название книги для поиска 😌')

    parse_dict, max_books = search_books(soup)  # Возвращаем словарь и кол-во найденных книг

    CURRENT_BOOK = hashlib.md5(
        message.text.encode()).hexdigest()  # Хешируем, чтобы обойти ограничение в 64 байта для CallbackData
    list_books = create_pages(parse_dict, max_books, 'books')  # Общий список книг
    current_page = get_page(items_list=list_books)
    await message.answer(current_page,
                         reply_markup=get_page_keyboard(
                             max_pages=len(list_books), key=CURRENT_BOOK, method='book'))


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
    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=list_books, page=current_page)

    markup = get_page_keyboard(max_pages=len(list_books), key=CURRENT_BOOK, page=current_page, method='book')
    await call.message.edit_text(current_page_text, reply_markup=markup)

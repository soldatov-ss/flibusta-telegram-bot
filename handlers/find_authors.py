import hashlib
import re

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.formats import get_language, languages_call
from keyboards.pagination import get_page_keyboard, pagination_call
from loader import dp
from utils.pages import create_pages, get_page
from utils.parsing.authors import search_authors, author_books, languages
from utils.parsing.general import get

list_authors = []
list_author_books = []
CURRENT_AUTHOR = ''
CURRENT_AUTHOR_BOOKS = ''
current_author_name = ''


@dp.message_handler(Command('author'))
async def author_search(message: types.Message):
    # Просто обработка сообщения /author + автор
    global CURRENT_AUTHOR, list_authors
    author = ' '.join(message.text.split()[1:])
    if not author:
        return await message.answer('Ничего нет 😕\n'
                                    'Попробуй так:\n'
                                    '/author <i>ФИО автора</i>')
    elif len(author) <= 2:
        return await message.answer('❗Слишком короткий запрос. Попробуй еще раз❗')

    url = f'http://flibusta.is//booksearch?ask={author}&cha=on'

    soup = await get(url)
    authors_dict, count_authors = search_authors(soup)
    list_authors = create_pages(authors_dict, count_authors, 'authors')
    current_page = get_page(list_authors)

    CURRENT_AUTHOR = hashlib.md5(
        message.text.encode()).hexdigest()
    await message.answer(current_page,
                         reply_markup=get_page_keyboard(
                             max_pages=len(list_authors), key=CURRENT_AUTHOR, method='author'))


@dp.message_handler(regexp=re.compile(r'^/a_\d+'))
async def chosen_link(message: types.Message):
    # Ловим линк и выводим доступные варинаты языков на которых написаны книги
    link = message.text.replace('_', '/')
    url = f'http://flibusta.is{link}&lang='
    # url = f'http://flibustahezeous3.onion{link}'

    soup = await get(url)
    abbr_lst, languages_lst = languages(soup)
    text = f'Книги доступны на следующих языках: \n' \
           f'Ты можешь выбрать удобный для тебя язык 👇'
    await message.answer(text, reply_markup=get_language(
        languages_lst=languages_lst, link=link, abbr_lst=abbr_lst))


@dp.callback_query_handler(languages_call.filter())
async def current_languages(call: types.CallbackQuery, callback_data: dict):
    # Вывод доступных книг по выбранному языку
    global current_author_name, list_author_books, CURRENT_AUTHOR_BOOKS

    language = callback_data['abbr']
    link = callback_data['link']

    url = f'http://flibusta.is{link}&lang={language}'
    soup = await get(url)

    author_books_dict, current_author_name = author_books(soup)
    count_books = len(author_books_dict.keys())

    list_author_books = create_pages(author_books_dict, max_books=count_books, flag='author_books')
    CURRENT_AUTHOR_BOOKS = link

    current_page = get_page(list_author_books, author=current_author_name)

    await call.message.answer(current_page, reply_markup=get_page_keyboard(
        max_pages=count_books, key=CURRENT_AUTHOR_BOOKS, method='author_books'))
    await call.answer(cache_time=60)


@dp.callback_query_handler(pagination_call.filter(page='current_page'))
async def current_page_error(call: types.CallbackQuery):
    # убираем часики по нажанию на текущую страницу
    await call.answer(cache_time=60)


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='author'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_AUTHOR:
        # Блокировка в предыдущем сообщении паганиции
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=list_authors, page=current_page)

    markup = get_page_keyboard(max_pages=len(list_authors), key=CURRENT_AUTHOR, page=current_page, method='author')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)


@dp.callback_query_handler(pagination_call.filter(method='author_books'))
async def show_chosen(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_AUTHOR_BOOKS:
        # Блокировка в предыдущем сообщении паганиции
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=list_author_books, author=current_author_name, page=current_page)

    markup = get_page_keyboard(max_pages=len(list_author_books), key=CURRENT_AUTHOR_BOOKS,
                               page=current_page, method='author_books')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)

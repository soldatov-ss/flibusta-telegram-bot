import hashlib

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.big_keyboard import get_big_keyboard, big_pagination
from keyboards.formats import languages_call
from keyboards.small_keyboard import get_small_keyboard, pagination_call
from loader import dp
from utils.pages import create_pages, get_page
from utils.parsing.authors import search_authors, author_books
from utils.parsing.general import get

AUTHORS_LST = []
AUTHOR_BOOKS_LST = []
CURRENT_AUTHOR = ''
CURRENT_AUTHOR_BOOKS = ''
current_author_name = ''
count_books = ''


@dp.message_handler(Command('author'))
async def author_command(message: types.Message):
    global CURRENT_AUTHOR, AUTHORS_LST
    author = ' '.join(message.text.split()[1:])

    if not author:
        return await message.answer('Ничего нет 😕\n'
                                    'Попробуй так:\n'
                                    '/author <i>ФИО автора</i>')
    elif len(author) <= 2:
        return await message.answer('❗Слишком короткий запрос. Попробуй еще раз❗')

    url = f'http://flibusta.is//booksearch?ask={author}&cha=on'

    soup = await get(url)
    try:
        authors_dict, count_authors = search_authors(soup)
    except AttributeError:
        return await message.answer('Ничего не найдено 😔\n'
                                    'Возможно ты ввел неправильно ФИО автора\n'
                                    'Попробуй еще раз 😊')

    AUTHORS_LST = create_pages(authors_dict, count_authors, 'authors')
    current_page = get_page(AUTHORS_LST)

    CURRENT_AUTHOR = hashlib.md5(
        author.encode()).hexdigest()
    await message.answer(current_page,
                         reply_markup=get_small_keyboard(
                             count_pages=len(AUTHORS_LST), key=CURRENT_AUTHOR, method='author'))


@dp.callback_query_handler(languages_call.filter())
async def current_languages(call: types.CallbackQuery, callback_data: dict):
    # Вывод список доступных книг по выбранному языку
    global current_author_name, AUTHOR_BOOKS_LST, CURRENT_AUTHOR_BOOKS, count_books

    language = callback_data['abbr']
    link = callback_data['link']

    url = f'http://flibusta.is{link}&lang={language}'
    soup = await get(url)

    author_books_dict, current_author_name = author_books(soup)
    count_books = len(author_books_dict.keys())

    AUTHOR_BOOKS_LST = create_pages(author_books_dict, count_items=count_books, flag='author_books')
    CURRENT_AUTHOR_BOOKS = link

    current_page = get_page(AUTHOR_BOOKS_LST, author=[current_author_name, count_books])

    await call.message.answer(current_page,
                              reply_markup=get_big_keyboard(count_pages=len(AUTHOR_BOOKS_LST),
                                                            key=CURRENT_AUTHOR_BOOKS, method='author_books'))
    await call.answer(cache_time=60)


@dp.callback_query_handler(pagination_call.filter(page='current_page'))
async def current_page_error(call: types.CallbackQuery):
    # убираем часики по нажанию на текущую страницу
    await call.answer(cache_time=60)


# Пагинация при показе всех доступных авторов
@dp.callback_query_handler(pagination_call.filter(method='author'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_AUTHOR:
        # Блокировка в предыдущем сообщении паганиции
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=AUTHORS_LST, page=current_page)

    markup = get_small_keyboard(count_pages=len(AUTHORS_LST), key=CURRENT_AUTHOR, page=current_page, method='author')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)


# Пагинация при показе всех доступных книг автора
@dp.callback_query_handler(big_pagination.filter(method='author_books'))
async def show_chosen(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_AUTHOR_BOOKS:
        # Блокировка в предыдущем сообщении паганиции
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(
        items_list=AUTHOR_BOOKS_LST, author=[current_author_name, count_books], page=current_page)
    print(len(AUTHOR_BOOKS_LST))
    markup = get_big_keyboard(count_pages=len(AUTHOR_BOOKS_LST), key=CURRENT_AUTHOR_BOOKS,
                              page=current_page, method='author_books')
    await call.message.edit_text(text=current_page_text, reply_markup=markup)

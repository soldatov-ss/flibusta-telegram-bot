import hashlib

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.small_keyboard import get_small_keyboard, pagination_call
from loader import dp
from utils.pages import create_pages, get_page
from utils.parsing.general import get
from utils.parsing.series import search_series
from utils.throttlig import rate_limit

CURRENT_SERIES = ''
CURRENT_SERIES_LIST = []


@rate_limit(limit=4)
@dp.message_handler(Command('series'))
async def series_command(message: types.Message):
    global CURRENT_SERIES, CURRENT_SERIES_LIST
    series_name = ' '.join(message.text.split()[1:])

    if not series_name:
        return await message.answer('Ничего нет 😕\n'
                                    'Попробуй так:\n'
                                    '/series <i>название серии</i>')
    if len(series_name) <= 2:
        return await message.reply('⛔ Слишком короткое название, попробуй еще раз')

    url = f'https://flibusta.is/booksearch?ask={series_name}&chs=on'
    soup = await get(url)

    try:
        series_dict, count_series = search_series(soup)
    except AttributeError:
        return await message.answer('Ничего не найдено 😔\n'
                                    'Возможно ты ввел неправильно название серии\n'
                                    'Попробуй еще раз 😊')

    CURRENT_SERIES_LIST = create_pages(books_dict=series_dict, count_items=count_series, flag='series')
    CURRENT_SERIES = hashlib.md5(
        series_name.encode()).hexdigest()

    current_page = get_page(CURRENT_SERIES_LIST)
    await message.answer(current_page,
                         reply_markup=get_small_keyboard(
                             count_pages=len(CURRENT_SERIES_LIST), key=CURRENT_SERIES, method='series'))


# Пагинация
@dp.callback_query_handler(pagination_call.filter(method='series'))
async def show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    if callback_data['key'] != CURRENT_SERIES:
        # Блокировка в предыдущем сообщении паганиции
        return await call.answer(cache_time=60)

    current_page = int(callback_data.get('page'))
    current_page_text = get_page(items_list=CURRENT_SERIES_LIST, page=current_page)

    markup = get_small_keyboard(
        count_pages=len(CURRENT_SERIES_LIST), key=CURRENT_SERIES, page=current_page, method='series')
    await call.message.edit_text(current_page_text, reply_markup=markup)

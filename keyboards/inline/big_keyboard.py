# Инлайн клавиатура для показа книг из серий т.к. их может быть больше 50 шт
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import dp

big_pagination = CallbackData('big_pagination', 'key', 'page', 'method')


@dp.callback_query_handler(big_pagination.filter(page='current_page'))
async def current_page_error(call: types.CallbackQuery):
    # убираем часики по нажанию на текущую страницу
    await call.answer(cache_time=60)


# Большая пагинация
def get_big_keyboard(count_pages: int, key, method, page: int = 1):
    first_page = '« 1'
    end_page = f'{count_pages} »'
    previous_page = page - 1
    next_page = page + 1
    pages_buttons = list()

    markup = InlineKeyboardMarkup()

    if page != 1 and count_pages > 2:
        pages_buttons.append(
            InlineKeyboardButton(
                text=first_page,
                callback_data=big_pagination.new(key=key, page=1, method=method)
            )
        )
    if previous_page >= 1:
        pages_buttons.append(
            InlineKeyboardButton(
                text=f'‹ {previous_page}',
                callback_data=big_pagination.new(key=key, page=page - 1, method=method)
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=f'- {page} -',
            callback_data=big_pagination.new(key=key, page='current_page', method=method)
        )
    )
    if next_page <= count_pages:
        pages_buttons.append(
            InlineKeyboardButton(
                text=f'{next_page} ›',
                callback_data=big_pagination.new(key=key, page=next_page, method=method)
            )
        )
    if page != count_pages and count_pages > 2:
        pages_buttons.append(
            InlineKeyboardButton(
                text=end_page,
                callback_data=big_pagination.new(key=key, page=count_pages, method=method)
            )
        )

    markup.row(*pages_buttons)
    return markup

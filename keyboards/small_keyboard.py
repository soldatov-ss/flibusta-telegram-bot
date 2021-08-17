from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

pagination_call = CallbackData('pagination', 'key', 'page', 'method')


def get_small_keyboard(count_pages: int, key, method, page: int = 1):
    previous_page = page - 1
    previous_page_text = 'Назад'
    current_page_text = f'{page}'
    next_page = page + 1
    next_page_text = 'Вперед'

    markup = InlineKeyboardMarkup()
    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page, method=method)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_call.new(key=key, page='current_page', method=method)
        )
    )

    if next_page <= count_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page, method=method)
            )
        )
    return markup

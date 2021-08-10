from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

files_call = CallbackData('file_btns', 'format_file', 'link')


def get_formats(formats_lst: list, link: str):
    markup = InlineKeyboardMarkup()

    for elem in formats_lst:
        markup.insert(
            InlineKeyboardButton(
                text=elem,
                callback_data=files_call.new(format_file=elem, link=link)
            )
        )
    return markup

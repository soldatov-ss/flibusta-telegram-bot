from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

files_call = CallbackData('file_btns', 'format_file', 'link')
languages_call = CallbackData('languages', 'language', 'link', 'abbr')
result_request = CallbackData('result_request', 'choice')


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



def get_language(languages_lst: list, link: str, abbr_lst):
    markup = InlineKeyboardMarkup()

    for elem in range(len(languages_lst)):
        lang = languages_lst[elem]
        abbr = abbr_lst[elem]
        markup.insert(
            InlineKeyboardButton(
                text=lang,
                callback_data=languages_call.new(language=elem, link=link, abbr=abbr)
            )
        )
    return markup



def get_requests(req_lst: list):
    markup = InlineKeyboardMarkup(row_width=2)

    for elem in req_lst:
        markup.insert(
            InlineKeyboardButton(
                text=elem,
                callback_data=result_request.new(choice=elem)
            )
        )
    return markup

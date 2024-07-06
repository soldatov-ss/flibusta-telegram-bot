from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DownloadCallbackData(CallbackData, prefix="download"):
    book_id: int
    file_format: str


def book_download_keyboard(file_formats: list, book_id: int):
    keyboard = InlineKeyboardBuilder()
    for file_format in file_formats:
        keyboard.button(text=file_format, callback_data=DownloadCallbackData(book_id=book_id, file_format=file_format))
    return keyboard.as_markup()

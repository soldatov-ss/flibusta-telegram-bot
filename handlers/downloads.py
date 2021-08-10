from aiogram import types
from aiogram.types import InputFile

from keyboards.formats import files_call
from loader import dp
from utils.parsing import get, description


@dp.callback_query_handler(files_call.filter())
async def download_book(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    format_file = callback_data['format_file']
    format_file_for_share = 'download' if format_file not in ['fb2', 'epub', 'mobi'] else format_file
    link = callback_data["link"]

    url = f'http://flibusta.is{link}/{format_file_for_share}'
    url_to_descr = f'http://flibusta.is{link}'
    soup = await get(url_to_descr)
    descr, author, book = description(soup)

    await call.message.answer('Ожидайте, начинаю скачивать книгу 🙃')
    await call.message.answer_document(
        InputFile.from_url(url, filename=f'{" ".join(book)}.{format_file}'), caption=author)

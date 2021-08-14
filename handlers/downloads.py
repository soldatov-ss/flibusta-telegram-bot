from io import BytesIO

from aiogram import types
from aiogram.types import InputFile

from keyboards.formats import files_call
from loader import dp
from utils.parsing.books import description
from utils.parsing.general import get, get_tempfile


@dp.callback_query_handler(files_call.filter())
async def download_book(call: types.CallbackQuery, callback_data: dict):
    format_file = callback_data['format_file']
    format_file_for_share = 'download' if format_file not in ['fb2', 'epub', 'mobi'] else format_file
    link = callback_data["link"]

    url = f'http://flibusta.is{link}/{format_file_for_share}'
    url_to_descr = f'http://flibusta.is{link}'
    soup = await get(url_to_descr)
    descr, author, book = description(soup)             # описание книги

    await call.message.answer(f'Ожидайте, начинаю скачивать книгу 🙃 {url}')

    response = await get_tempfile(url)
    res_to_bytesio = BytesIO(response.read())       # конвентируем книгу в байты для отправки
    file = InputFile(path_or_bytesio=res_to_bytesio, filename=f'{" ".join(book)}.{format_file}')

    await call.message.answer_document(file, caption=author)
    await call.answer(cache_time=60)
    response.close()

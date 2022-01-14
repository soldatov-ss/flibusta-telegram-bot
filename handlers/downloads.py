from io import BytesIO

from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.exceptions import NetworkError, InvalidQueryID

from keyboards.inline.formats import files_call
from loader import dp, db
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
    descr, author, book = description(soup)  # описание книги

    wait = await call.message.answer(f'Ожидайте, начинаю скачивать книгу 🙃 {url}')

    response = await get_tempfile(url)
    res_to_bytesio = BytesIO(response.read())  # конвентируем книгу в байты для отправки
    file = InputFile(path_or_bytesio=res_to_bytesio, filename=f'{book}.{format_file}')

    try:
        await call.message.answer_document(file, caption=author)
    except NetworkError:  # Ловим ограничение по отправке файлов весом больше 50 метров
        await wait.edit_text(f'Не могу отправить файл😔\n'
                             f'Попробуй скачать по ссылке:\n'
                             f'{url}')
    try:
        await call.answer(cache_time=60)
    except InvalidQueryID:  # Ловим ошибку на длительную скачивание/отправку
        pass

    await db.rating_book(book=book, link=link)  # добавляем в базу данных (для составления рейтинга скачанных книг)
    response.close()

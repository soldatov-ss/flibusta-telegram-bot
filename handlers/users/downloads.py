from io import BytesIO

from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.exceptions import NetworkError, InvalidQueryID, BadRequest

from handlers.users.chosen_links import get_book_description
from keyboards.inline.other_keyboards import files_call
from loader import dp, db
from utils.parsing.general import get_tempfile
from utils.throttlig import rate_limit


def get_callback_data(callback_data: dict):
    if callback_data['format_file'] not in ['fb2', 'epub', 'mobi']:
        format_file = 'download'
    else:
        format_file = callback_data['format_file']

    link = callback_data["link"]
    return format_file, link


@rate_limit(limit=5, key='downloading')
@dp.callback_query_handler(files_call.filter())
async def download_book(call: types.CallbackQuery, callback_data: dict):
    format_file, link = get_callback_data(callback_data)

    url = f'http://flibusta.is{link}/{format_file}'
    book, author, *args = await get_book_description(link)

    file_id = await db.select_file_id(link=link, format=format_file)
    message = await call.message.answer(f'Ожидайте, начинаю скачивать книгу 🙃')
    if file_id:
        try:
            await call.message.answer_document(file_id, caption=author)
            await call.answer()
        except BadRequest:
            pass
        except TimeoutError:
            print('here')
    else:
        file = await get_file(message, callback_data['format_file'], url, book)
        if not file: return

        try:
            future_file_id = await call.message.answer_document(file, caption=author)
            await call.answer()
            file_id = future_file_id.document.file_id

        except NetworkError:  # Ловим ограничение по отправке файлов весом больше 50 метров
            return await message.edit_text(f'Не могу отправить файл т.к. в телеграме есть огранчиния по весу файлов😔\n'
                                           f'Попробуй скачать по ссылке:\n'
                                           f'{url}')
        except InvalidQueryID:  # Ловим ошибку на длительную скачивание/отправку
            pass



        await db.insert_file_id(link=link, format=format_file, file_id=file_id)

    await db.update_count_downloaded(link=link)  # кол-во скачиваний
    await db.update_user_downloads(user_id=call.from_user.id) # кол-во загрузок у юзера
    await message.delete()


async def get_file(message: types.Message, format_file: str, url: str, book: str):
    '''
    Получаем временный файл и конвертируем в байты для отправки
    '''
    response = await get_tempfile(url)
    try:
        res_to_bytesio = BytesIO(response.read())  # конвентируем книгу в байты для отправки

        file = InputFile(path_or_bytesio=res_to_bytesio, filename=f'{book}.{format_file}')

    except AttributeError:

        await message.edit_text('Упс! Возникли небольшие неполадки на сервере 😲\n'
                                       'Попробуй скачать книгу в другом формате 🙌\n')
        return
    finally:
        response.close()

    return file

import logging
import re

from aiogram import Router, F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram_widgets.pagination import TextPaginator

from infrastructure.database.service import get_repository
from infrastructure.service.books_service import BookService
from tgbot.keyboards.inline import DownloadCallbackData, book_download_keyboard
from tgbot.misc.book_utils import get_book_file, is_file_size_valid, clean_html
from tgbot.misc.formatter import book_formatter

books_router = Router()
logger = logging.getLogger(__name__)


@books_router.message(F.text.regexp(r"^/book_(\d+)").as_("digits"))
async def book_detail_handler(message: types.Message, digits: re.Match[str]):
    if digits.group():
        book_id = int(digits.group().split('_')[1])

        async with get_repository() as repo:
            book_service = BookService(session=repo.session)
            book = await book_service.get_full_book_info(book_id)
            if not book:
                return await message.reply("Book not found.")

            text = f'📖 <b>{book.title}</b>\n' \
                   f'<i>{book.authors}</i>\n' \
                   f'{book.sequences} \n' \
                   f'<i>{book.genres}</i>\n\n' \
                   f'{clean_html(book.body) if book.body else "There is no description"}'[:4095]

            formats = book_service.get_book_file_formats(book)
            keyboard = book_download_keyboard(formats, book_id)
            await message.reply(text, parse_mode='HTML', reply_markup=keyboard)
    else:
        await message.reply('Invalid book id!')


@books_router.message(F.text, StateFilter(None))
async def handle_books_by_title(message: types.Message):
    async with get_repository() as repo:
        book_service = BookService(session=repo.session)
        try:
            books = await book_service.get_books_with_authors_by_title(message.text.strip())
        except Exception as e:
            logging.error(f"Failed to fetch books: {message.text.strip()}. Error: {e}")
            return await message.answer("Failed to retrieve book data. Please try again later.")

        if not books:
            return await message.answer("No books found with the specified title.")

        text_data = []
        for i, book in enumerate(books, start=1):
            is_first_page = i == 1
            authors = ', '.join(book.authors) if book.authors else "Unknown Author"
            link = f"/book_{book.book_id}"

            page_text = book_formatter(len(books), authors, book, link, is_first_page)
            text_data.append(page_text)

        paginator = TextPaginator(
            data=text_data,
            router=books_router,
            join_symbol="\n\n",
        )
        current_text_chunk, reply_markup = paginator.current_message_data

        await message.answer(
            text=current_text_chunk,
            reply_markup=reply_markup,
        )


@books_router.callback_query(DownloadCallbackData.filter())
async def download_book(query: CallbackQuery, callback_data: DownloadCallbackData):
    await query.answer()

    book_id = callback_data.book_id
    file_format = callback_data.file_format

    async with get_repository() as repo:
        book_service = BookService(session=repo.session)
        book = await book_service.get_full_book_info(book_id)
        if not book:
            logger.error(f"Book with ID {book_id} not found during downloading.")
            return await query.message.reply("Book not found.")

        if not is_file_size_valid(book.file_size):
            return await query.message.edit_text(f'The file size is too big. Try download from flibusta site')

    message = await query.message.edit_text(f'Started downloading the book. Book id: {book_id}')

    try:
        book_file = await get_book_file(book, file_format)
        await query.message.answer_document(document=book_file, caption=book.title)
        await message.delete()
    except Exception as e:
        logger.error(f"Error downloading book with ID {book.book_id} format: {file_format}: {e}")
        await query.message.edit_text(f"Error downloading the book. Book: {book.title}. Try again later.")

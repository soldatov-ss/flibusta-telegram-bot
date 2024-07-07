import logging
import re

from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from infrastructure.database.service import get_repository
from infrastructure.service.books_service import BookService
from tgbot.keyboards.inline import DownloadCallbackData, book_download_keyboard
from tgbot.keyboards.paginator import handle_pagination
from tgbot.misc.book_utils import is_file_size_valid
from tgbot.misc.formatter import book_formatter, detailed_book_formatter

books_router = Router()
logger = logging.getLogger(__name__)


@books_router.message(F.text.regexp(r"^/book_(\d+)").as_("digits"))
async def book_detail_handler(message: types.Message, digits: re.Match[str]):
    if digits.group():
        book_id = int(digits.group().split("_")[1])

        async with get_repository() as repo:
            book_service = BookService(session=repo.session)
            book = await book_service.get_full_book_info(book_id)
            if not book:
                return await message.reply("Book not found.")

            formats = book_service.get_book_file_formats(book)
            keyboard = book_download_keyboard(formats, book_id)
            await message.reply(detailed_book_formatter(book), parse_mode="HTML", reply_markup=keyboard)
    else:
        await message.reply("Invalid book id!")


@books_router.message(F.text, StateFilter(None))
async def handle_books_by_title_handler(message: types.Message):
    async with get_repository() as repo:
        book_service = BookService(session=repo.session)
        try:
            books = await book_service.get_books_with_authors_by_title(message.text.strip())
        except Exception as e:
            logger.error(f"Failed to fetch books: {message.text.strip()}. Error: {e}")
            return await message.answer("Failed to retrieve book data. Please try again later.")

        if not books:
            return await message.answer("No books found with the specified title.")

        books_data = [
            (", ".join(book.authors) if book.authors else "Unknown Author", book, f"/book_{book.book_id}", i == 0)
            for i, book in enumerate(books)
        ]
        text_data: list[str] = [book_formatter(len(books), *item) for item in books_data]
        await handle_pagination(message, text_data, books_router)


@books_router.callback_query(DownloadCallbackData.filter())
async def download_book_handler(query: CallbackQuery, callback_data: DownloadCallbackData):
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
            return await query.message.edit_text("The file size is too big. Try download from flibusta site")

    message = await query.message.edit_text(f"Started downloading the book. Book id: {book_id}")
    try:
        file = await book_service.get_book_file_id(book, file_format)
        sent_message = await query.message.answer_document(file, caption=book.title)
        await repo.users.proceed_user_download_book(
            query.from_user.id, book_id, sent_message.document.file_id, file_format
        )

        await message.delete()
    except Exception as e:
        logger.error(f"Error downloading book with ID {book.book_id} format: {file_format}: {e}")
        await query.message.edit_text(f"Error downloading the book. Book: {book.title}. Try again later.")

import logging

from aiogram import Router, F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram_widgets.pagination import TextPaginator

from infrastructure.database.service import get_repository
from infrastructure.service.books_service import BookService
from tgbot.misc.formatter import book_formatter

books_router = Router()
logger = logging.getLogger(__name__)


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

            page_text = book_formatter(len(books), authors, book.title, link, is_first_page)
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

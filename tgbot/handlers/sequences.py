import logging
import re

from aiogram import F, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message

from infrastructure.database.service import get_repository
from infrastructure.service.books_service import BookService
from tgbot.keyboards.paginator import handle_pagination
from tgbot.misc.formatter import books_by_sequence_formatter, sequence_formatter
from tgbot.misc.message_factory import get_missing_book_sequence_args_message

sequence_router = Router()

logger = logging.getLogger(__name__)


@sequence_router.message(F.text.regexp(r"^/sequence_(\d+)").as_("digits"))
async def sequence_detail_handler(message: Message, digits: re.Match[str]):
    if digits.group():
        sequence_id = int(digits.group().split("_")[1])

        async with get_repository() as repo:
            book_service = BookService(session=repo.session)
            try:
                sequence_name, books, author = await book_service.get_books_by_sequence(sequence_id)
            except Exception as e:
                logger.error(f"Failed to fetch sequence by name: {message.text.strip()}. Error: {e}")
                return await message.answer("Failed to retrieve sequence data by name. Please try again later.")

            if not books:
                return await message.answer("No books found with the specified sequence name.")

            books_data = [
                (book, f"/book_{book.book_id}", i == 0)
                for i, book in enumerate(books)
            ]
            text_data: list[str] = [
                books_by_sequence_formatter(len(books), author, sequence_name, *item)
                for item in books_data
            ]
            await handle_pagination(message, text_data, sequence_router)
    else:
        await message.reply("Invalid sequence id!")


@sequence_router.message(F.text, Command("sequence"))
async def handle_sequences_by_name_handler(message: Message, command: CommandObject):
    if command.args is None:
        return await message.reply(get_missing_book_sequence_args_message())

    async with get_repository() as repo:
        try:
            book_sequences = await repo.sequences.get_sequences_by_name(command.args)
        except Exception as e:
            logger.error(f"Failed to fetch sequences: {command.args}. Error: {e}")
            return await message.answer("Failed to retrieve sequences data. Please try again later.")

        if not book_sequences:
            return await message.answer("No book sequences found with the specified name.")

        sequence_data = [
            (sequence, f"/sequence_{sequence.seq_id}", i == 0)
            for i, sequence in enumerate(book_sequences)
        ]
        text_data: list[str] = [sequence_formatter(len(book_sequences), *item) for item in sequence_data]
        await handle_pagination(message, text_data, sequence_router)

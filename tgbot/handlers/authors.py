import logging

from aiogram import F, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message

from infrastructure.database.service import get_repository
from tgbot.keyboards.paginator import handle_pagination
from tgbot.misc.formatter import author_formatter
from tgbot.misc.message_factory import get_author_missing_args_message

author_router = Router()

logger = logging.getLogger(__name__)


@author_router.message(F.text, Command("author"))
async def handle_authors_by_name_handler(message: Message, command: CommandObject):
    if command.args is None:
        return await message.reply(get_author_missing_args_message())

    async with get_repository() as repo:
        try:
            authors = await repo.authors.get_authors_by_name(command.args)
        except Exception as e:
            logger.error(f"Failed to fetch authors: {command.args}. Error: {e}")
            return await message.answer("Failed to retrieve authors data. Please try again later.")

        if not authors:
            return await message.answer("No authors found with the specified name.")

        authors_data = [(author, f"/author_{author.author_id}", i == 0) for i, author in enumerate(authors)]
        text_data: list[str] = [author_formatter(len(authors), *item) for item in authors_data]
        await handle_pagination(message, text_data, author_router)

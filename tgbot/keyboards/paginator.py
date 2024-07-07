import logging

from aiogram import Router
from aiogram.types import Message
from aiogram_widgets.pagination import TextPaginator

logger = logging.getLogger(__name__)


async def handle_pagination(message: Message, text_data: list[str], router: Router) -> None:
    try:
        paginator = TextPaginator(data=text_data, router=router, join_symbol="\n\n")
        current_text_chunk, reply_markup = paginator.current_message_data
        await message.answer(text=current_text_chunk, reply_markup=reply_markup)
    except Exception as e:
        logger.error(e)

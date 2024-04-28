import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from infrastructure.database.service import get_repository

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        async with get_repository() as repo:
            user = await repo.users.get_or_create_user(
                event.message.from_user.id,
                event.message.from_user.full_name,
                event.message.from_user.language_code,
                event.message.from_user.username
            )
            # data["session"] = session
            data["repo"] = repo
            data["user"] = user

            result = await handler(event, data)
        return result

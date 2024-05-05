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
            event_from_user = data.get("event_from_user")
            user = await repo.users.get_or_create_user(
                event_from_user.id,
                event_from_user.full_name,
                event_from_user.language_code,
                event_from_user.username,
            )
            data["repo"] = repo
            data["user"] = user

            result = await handler(event, data)
        return result

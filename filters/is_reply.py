from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class IsReplyFilter(BoundFilter):
    """
    Фильтр, проверяющий, является ли сообщение ответом на сообщение
    """

    key = "is_reply"
    is_reply: bool

    async def check(self, message: types.Message) -> bool:
        return self.is_reply and message.reply_to_message
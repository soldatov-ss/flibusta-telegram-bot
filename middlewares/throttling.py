import asyncio
from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import exceptions
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.service_text = '❗Слишком часто!\nДавай не так быстро'
        super(ThrottlingMiddleware, self).__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        if getattr(handler, 'override', None) == message.from_user.id:
            return
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    # noinspection PyUnusedLocal
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        if getattr(handler, 'override', None) == cq.from_user.id:
            return
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.callback_query_throttled(cq, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        if handler:
            text = getattr(handler, "throttling_text", self.service_text)
        else:
            text = self.service_text

        if throttled.exceeded_count <= 2:
            service_message = await message.reply(text)

            await asyncio.sleep(5)
            await service_message.delete()
        try:
            await message.delete()
        except Exception as err:
            pass

    async def callback_query_throttled(self, cq: types.CallbackQuery, throttled: Throttled):
        handler = current_handler.get()

        if handler:
            text = getattr(handler, "throttling_text", self.service_text) or 'Too many requests!'
        else:
            text = self.service_text or 'Too many requests!'

        if throttled.exceeded_count <= 2:
            with suppress(exceptions.InvalidQueryID):
                await cq.answer(text, show_alert=True)

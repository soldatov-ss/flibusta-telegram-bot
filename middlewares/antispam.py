from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class CheckTypeMessage(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict):
        '''
        Ограничение для юзеров, чтобы не слали в группу аудио/стикеры
        '''
        if update.message:
            if not update.message.text and not update.message.photo:
                await update.message.delete()
                return
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot


class IsGroup(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsBot(BoundFilter):
    '''
     Фильтр на сообщения, чтобы в группу не писали другие боты
    '''
    async def check(self, message: types.Message):
        isBot = message.from_user.is_bot
        if isBot and message.from_user.username != 'GroupAnonymousBot':
            await bot.kick_chat_member(message.chat.id, message.from_user.id)
            await message.answer(f'Пользователь {message.from_user.get_mention()} был кикнут!\n'
                                 f'Причина: в группе могут находится только люди 🤖')

        return True if not isBot else False
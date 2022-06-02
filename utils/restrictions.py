from aiogram import types

from loader import bot
from utils.pages.strings import no_result_message, message_into_bot



class CheckFromUser:
    '''
    Класс который создает ограничения в боте на доступность контента
    В группах же ограничений нет
    '''

    def __init__(self, chat: types.Chat, url: str, function: callable, method: str):

        self.method = method
        self.function = function
        self.url = url
        self.chat = chat
        self.text = None
        self.soup_without_register = None
        self.soup_with_register = None

    async def check_chat_type(self):

        if self.chat.type == 'private':
            self.soup_without_register = await bot.get('session').get_soup(self.url)
            return await self.result_for_user_in_privatChat()
        else:
            self.soup_with_register = await bot.get('session').get_soup(self.url)
            return await self.result_for_user_in_group()


    async def result_for_user_in_privatChat(self):
        data_without_register = self.function(self.soup_without_register)

        if data_without_register:
            self.text = message_into_bot(self.method)
            await self.send_message()
            return data_without_register
        else:
            self.text = no_result_message(method=self.method)
            await self.send_message()
            return None


    async def result_for_user_in_group(self):
        # Все доступные книги, если запрос пришел с группы
        data_with_register = self.function(self.soup_with_register)

        if not data_with_register:
            self.text = no_result_message(method=self.method)
            await self.send_message()
        else:
            return data_with_register


    async def send_message(self):
        await bot.send_message(self.chat.id, self.text)


    async def result_for_series_book(self, link: str):
        # Возвращает все книги по выбранной книжной серии

        self.soup_with_register = await bot.get('session').get_soup(self.url)
        book_dct, count_books = await self.function(self.soup_with_register, link)

        return book_dct, count_books, self.soup_with_register

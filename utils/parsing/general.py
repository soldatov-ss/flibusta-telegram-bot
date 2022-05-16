import tempfile

import aiohttp
import fake_useragent
from aiogram import types
from bs4 import BeautifulSoup

import config

user = fake_useragent.UserAgent().random
url_to_register = 'http://flibusta.is/user'
headers = {'user-agent': user}
data = {
    'name': config.CITE_LOGIN,
    'pass': config.CITE_PASS,
    'form_id': 'user_login',
}


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_to_register, headers=headers, data=data):  # Авторизация на сайте
            async with session.get(url, headers=headers) as response:
                res = await response.text()
                soup = BeautifulSoup(res, 'lxml')
                return soup


async def get_tempfile(url):
    # Функция нужна для того чтобы скачивать временный файл, т.к.
    # с помощью методов аиограмма не получится скачивать некоторые файлы, ибо нужна авторизация на сайте
    async with aiohttp.ClientSession() as session:
        async with session.post(url_to_register, headers=headers, data=data):
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    fp = tempfile.TemporaryFile()
                    fp.write(await response.read())
                    fp.seek(0)
                    return fp


async def get_without_register(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = await response.text()
            soup = BeautifulSoup(res, 'lxml')
            return soup



async def check_chat_type(chat: types.Chat, url: str):
    '''
    :return: object of BeautifulSoup
    '''
    if chat.type == 'private':
        soup = await get_without_register(url)
    else:
        soup = await get(url)
    return soup
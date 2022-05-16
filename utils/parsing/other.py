from aiogram import types

from utils.pages.strings import no_result_message
from utils.parsing.books import parsing_formats, description
from utils.parsing.general import get, check_chat_type


async def get_book_description(link):
    '''
    Проверяем есть ли описание к книге в БД, если нет - парсим и добавляем в БД
    :param link: str
    :return: list with description about book
    '''
    from loader import db

    url = f'http://flibusta.is{link}'
    data = await db.select_book(link=link)

    if data and data.get('description'):

        descr = data.get('description')
        author = data.get('author')
        book = data.get('book_name')
        formats_list = data.get('formats').split(':')
    else:
        soup = await get(url)
        formats_list = parsing_formats(soup)

        descr, author, book = description(soup)
        formats = ':'.join(formats_list)
        await db.insert_book(book=book, link=link, author=author, formats=formats, description=descr)

    descr = descr[:3*1000].replace('<', '(').replace('>', ')') # Ограничение на длинну текста и убраны скобки, чтобы не падал бот при выводе
    return book, author, formats_list, descr



async def create_list_choices(message: types.Message):
    '''
    Возвращает список вариантов для инлайн клавиатуры в main_handler
    :return list of buttons
    '''
    url = f'http://flibusta.is//booksearch?ask={message.text}&chs=on&cha=on&chb=on'
    soup = await check_chat_type(message.chat, url)

    result = []
    for i in soup.find_all('h3'):
        if not i.text.split()[1] in ('серии', 'писатели', 'книги'):
            continue
        if i.text.split()[1] == 'серии':
            result.append('Книжные серии')
        else:
            result.append(i.text.split()[1].title())

    if not result:
        empty_message = no_result_message(method='book')
        await message.answer(empty_message)
        return

    return result
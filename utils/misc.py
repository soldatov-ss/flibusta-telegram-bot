from loader import bot
from utils.parsing.authors import search_authors, author_books
from utils.parsing.books import search_books
from utils.parsing.general import get, get_without_register


def check_link(link):
    # /b_101112@my_flibusta_bot
    link = link.replace('_', '/')
    if '@' in link:
        link = link[:link.find('@')]
    # /b/101112
    return link


async def check_group_or_bot(chat_id, url):
    soup_with = await get(url)
    if str(chat_id) == '415348636':  # чат айди, если запрос пришел с бота, а не с группы
        soup_without = await get_without_register(url)

        if not search_books(soup_with):
            text = 'По запросу ничего не найдено! 😔\n' \
                   'Введи название книги для поиска 😌'
            await bot.send_message(chat_id, text)
            return False
        elif not search_books(soup_without) and search_books(soup_with):
            text = '<b>❗Во избежание блокировки бота за нарушение авторских прав❗</b>\n' \
                   f'Многие книги могут быть недоступны 😔\n' \
                   f'Книги по Вашему запросу доступны в группе: @free_book_flibusta\n\n' \
                   f'Приносим извинения за все неудобства😇'
            await bot.send_message(chat_id, text)
            return False
        elif search_books(soup_without):
            text = f'Больше книг доступно в группе -- @free_book_flibusta 📚'
            await bot.send_message(chat_id, text)

            book_dict_without, count_books_without = search_books(soup_without)
            return book_dict_without, count_books_without, 'bot'
    else:
        if not search_books(soup_with):
            text = 'По запросу ничего не найдено! 😔\n' \
                   'Введи название книги для поиска 😌'
            await bot.send_message(chat_id, text)
            return False
        else:
            book_dict_with, count_books_with = search_books(soup_with)
            return book_dict_with, count_books_with, 'group'


async def check_group_or_bot_for_author(chat_id, url):
    soup_with = await get(url)
    if str(chat_id) == '415348636':  # чат айди, если запрос пришел с бота, а не с группы
        soup_without = await get_without_register(url)

        if not search_authors(soup_with):
            text = 'Ничего не найдено 😔\n' \
                   'Возможно ты ввел неправильно ФИО автора\n' \
                   'Попробуй еще раз 😊'
            await bot.send_message(chat_id, text)
            return False
        elif not search_authors(soup_without) and search_authors(soup_with):
            text = '<b>❗Во избежание блокировки бота за нарушение авторских прав❗</b>\n' \
                   f'Многие авторы и книги могут быть недоступны 😔\n' \
                   f'Авторы по Вашему запросу доступны в группе: @free_book_flibusta\n\n' \
                   f'Приносим извинения за все неудобства😇'
            await bot.send_message(chat_id, text)
            return False
        elif search_authors(soup_without):
            text = f'Больше авторов доступно в группе -- @free_book_flibusta 📚'
            await bot.send_message(chat_id, text)

            authors_dict_without, count_authors_without = search_authors(soup_without)
            return authors_dict_without, count_authors_without, 'bot'
    else:
        if not search_authors(soup_with):
            text = 'Ничего не найдено 😔\n' \
                   'Возможно ты ввел неправильно ФИО автора\n' \
                   'Попробуй еще раз 😊'
            await bot.send_message(chat_id, text)
            return False
        else:
            authors_dict_with, count_authors_with = search_authors(soup_with)
            return authors_dict_with, count_authors_with, 'group'


async def check_group_or_bot_for_author_books(call, url):
    soup_with = await get(url)

    if call.find('-1001572945629') == -1:
        soup_without = await get_without_register(url)

        if not author_books(soup_without) and author_books(soup_with):
            text = '<b>❗Во избежание блокировки бота за нарушение авторских прав❗</b>\n' \
                   f'Многие книги могут быть недоступны 😔\n' \
                   f'Книги по Вашему запросу доступны в группе: @free_book_flibusta\n\n' \
                   f'Приносим извинения за все неудобства😇'
            await bot.send_message(-1001572945629, text)
            return False

        elif author_books(soup_without):
            book_dict_without, count_books_without, author = author_books(soup_without)
            return book_dict_without, count_books_without, 'bot', author

    else:
        book_dict_with, count_books_with, author = author_books(soup_with)
        return book_dict_with, count_books_with, 'group', author

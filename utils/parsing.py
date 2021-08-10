import aiohttp
import fake_useragent
from bs4 import BeautifulSoup
import config


async def get(url):
    user = fake_useragent.UserAgent().random
    url_to_register = 'http://flibusta.is/user'
    headers = {'user-agent': user}
    data = {
        'name': config.CITE_LOGIN,
        'pass': config.CITE_PASS,
        'form_build_id': config.FORM_BUILD_ID,
        'form_id': 'user_login',
        'op': 'Вход в систему'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url_to_register, headers=headers, data=data):  # Авторизация на сайте
            async with session.get(url, headers=headers) as response:
                res = await response.text()
                soup = BeautifulSoup(res, 'lxml')
                return soup


def find_pagination(soup):
    # Проверяем на наличие страниц пагинанации
    # Не знаю нужна ли пагинация по страницам или достаточно 50 вариантов книг с первой страницы
    try:
        pagination_ul = soup.find('div', class_='item-list').find('ul', class_='pager').find_all('li')
    except AttributeError:
        return None
    list_pages = []

    if pagination_ul:
        for li in pagination_ul:
            number_page = li.find('a')
            if number_page:
                if number_page.text.isdigit():
                    list_pages.append(number_page.text)
    # Возврат списка с нумерацией страниц
    return list_pages


def parse_flibusta(soup):
    # Парсим все названия книг, авторов и ссылки с первой страницы
    block = soup.find('div', id='main')
    try:
        ul = block.find('h3').find_next().find_all('li')
    except AttributeError:
        return False

    dict_books_links = {}

    for li in ul:
        book = li.find_all('a')[0].text
        link = li.find('a').get('href')
        try:
            author = li.find_all('a')[1].text
        except IndexError:
            author = 'no-name'

        dict_books_links[link] = []
        dict_books_links[link].append(book)
        dict_books_links[link].append(author)
        # dict_books_links = {link: [book, author]}

    max_books = len(dict_books_links)
    return dict_books_links, max_books


def parsing_formats(soup):
    # Парсим страницу на доступные форматы
    formats_list = ['fb2', 'epub', 'mobi', '(скачать pdf)', '(скачать djvu)']
    formats_from_page = []
    ul = soup.find('select', id='useropt')
    if ul:
        # Проверка на наличие fb2/epub/mobi
        formats_from_page = [elem.text for elem in ul if elem.text in formats_list]
    else:
        # Проверка на наличие pdf/djvu
        ul = soup.find('div', id='main').find_all('a')
        for a in ul:
            elem = a.text
            if elem in formats_list:
                elem = elem[1:-1].split()[1]
                formats_from_page.append(''.join(elem))
    return formats_from_page


def description(soup):
    # Парсим описание книги
    text = soup.find('h2', text='Аннотация').find_next().text
    author = soup.find('h1', class_='title').find_next().find_next().text
    book = soup.find('h1', class_='title').text

    formats_lst = ['(fb2)', '(epub)', '(mobi)', '(pdf)', '(djvu)']
    book = book.split()[:-1] if list(book.split())[-1] in formats_lst else book
    if not text:
        text = 'Описание отсутствует'
    elif not author:
        author = 'Автор отсутствует'
    return text, author, book

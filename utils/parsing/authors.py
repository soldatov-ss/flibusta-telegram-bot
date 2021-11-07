def search_authors(soup):
    # Ищем всех авторов по запросу
    try:
        res = soup.find('div', id='main').find('h3').find_next().find_all('li')
    except AttributeError:
        return None
    authors_dict = {}
    for li in res:
        link = li.find('a').get('href')
        author = li.text
        authors_dict[link] = author
    count_authors = len(authors_dict.keys())
    return authors_dict, count_authors


def author_books(soup):
    # Ищем все книги и линки принадлежащие автору
    res = soup.find('div', id='main').find_all('form', method='POST')
    author = soup.find('h1', class_='title').text
    books_dict = {}
    for items in res:
        for item in items.find_all('a'):
            link = item.get('href')
            if link.startswith('/b/') and not link.endswith(('download', 'read', 'mail')):
                if item.text not in ('(fb2)', '(epub)', '(mobi)'):
                    books_dict[link] = item.text
    return books_dict, len(books_dict.keys()), author


def languages(soup):
    # Проверяем есть ли книги у автора на трех языках или менее 3-х
    abbr_lang, only_three_lang = [], []
    res = soup.find('div', id='main').find('select')
    variables_lang = [lang.text for lang in res][1:]

    author = soup.find('h1', class_='title').text

    for item in variables_lang:
        abbr = item.split()[1].replace('(', '').replace(')', '')  # Абревиатура языка
        lang = item.split()[0].title()

        if len(variables_lang) <= 3:
            only_three_lang.append(lang)
            abbr_lang.append(abbr)

        elif abbr in ['ru', 'uk', 'en'] and len(variables_lang) > 3:
            only_three_lang.append(lang)
            abbr_lang.append(abbr)

    return abbr_lang, only_three_lang, author

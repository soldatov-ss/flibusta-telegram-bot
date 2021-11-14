def book_strings(count_books, author, book, link):
    link = link[1:].replace('/', '_', 1)
    url = 'https://flibusta.is/booksearch?ask=&chb=on'

    if count_books >= 50:
        first_text = f'🔎  Найдено всего книг: >= {count_books}  🔍\n\n' \
                     f'❗<i>По запросу найдено более 50 книг\n' \
                     f'Для удобства выведены первые 50\n' \
                     f'Остальные книги доступны на сайте: {url}</i>\n\n' \
                     f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                     f'⬇ Скачать: /{link}\n\n'
    else:
        first_text = f'🔎  Найдено всего книг: {count_books}  🔍\n\n' \
                     f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                     f'⬇ Скачать: /{link}\n\n'

    other_text = f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                 f'⬇ Скачать: /{link}\n\n'
    return first_text, other_text


def author_strings(count_books, author, link):
    link = link[1:].replace('/', '_', 1)
    url = 'https://flibusta.is/booksearch?ask=&cha=on'
    if count_books >= 50:
        first_text = f'🔎 Авторов по запросу найдено: >= {count_books} 🔍\n\n' \
                     f'❗<i>По запросу найдено более 50 авторов\n' \
                     f'Для удобства выведены первые 50\n' \
                     f'Остальные авторы доступны на сайте: {url}</i>\n\n' \
                     f'<b>{author}</b> \n' \
                     f'Книги автора: 📚 /{link}\n\n'
    else:
        first_text = f'🔎 Авторов по запросу найдено: {count_books} 🔍\n\n\n' \
                     f'<b>{author}</b>\n' \
                     f'Книги автора: 📚/{link}\n\n'

    other_text = f'<b>{author}</b>\n' \
                 f'Книги автора: 📚/{link}\n\n'

    return first_text, other_text


def author_books_strings(book, link):
    link = link[1:].replace('/', '_', 1)

    text = f'📖<b>{book}</b>\n' \
           f'⬇Скачать книгу: /{link}\n\n'

    return text


def series_strings(count_series, series, link):
    link = link[1:].replace('/', '_', 1)

    first_text = f'🔎 Найдено совпадений: {count_series} 🔍\n\n' \
                 f'📚<b>{series}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    other_text = f'📚<b>{series}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    return first_text, other_text


def series_book_strings(count_book, book, link):
    link = link[1:].replace('/', '_', 1)

    first_text = f'📚Найдено книг: {count_book}\n\n' \
                 f'📖<b>{book}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    other_text = f'📖<b>{book}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    return first_text, other_text


def strings_for_user_into_bot(danger_message=None, second_message=None, no_result_message=None):
    if danger_message:
        text = '<b>❗Во избежание блокировки бота за нарушение авторских прав❗</b>\n' \
               f'Многие книги и авторы могут быть недоступны 😔\n' \
               f'Книги по Вашему запросу доступны в группе: @free_book_flibusta\n\n' \
               f'Приносим извинения за все неудобства😇'

    if second_message == 'series':
        text = f'Больше книжных серий доступно в группе -- @free_book_flibusta 📚'
    elif second_message == 'authors':
        text = f'Больше авторов доступно в группе -- @free_book_flibusta 📚'
    elif second_message == 'books':
        text = f'Больше книг доступно в группе -- @free_book_flibusta 📚'

    if no_result_message == 'series':
        text = 'Ничего не найдено 😔\n' \
               'Возможно ты ввел неправильно название книжной серии\n' \
               'Попробуй еще раз 😊'
    elif no_result_message == 'author':
        text = 'Ничего не найдено 😔\n' \
               'Возможно ты ввел неправильно ФИО автора\n' \
               'Попробуй еще раз 😊'
    elif no_result_message == 'books':
        text = 'По запросу ничего не найдено! 😔\n' \
               'Введи название книги для поиска 😌'
    return text

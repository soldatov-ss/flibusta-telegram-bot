from aiogram.utils.markdown import hlink


def book_strings(count_books, author, book, link):
    link = link[1:].replace('/', '_', 1)
    operand = ':' if count_books < 50 else '>'

    first_text = f'🔎  Найдено всего книг {operand} {count_books}  🔍\n\n' \
                 f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                 f'⬇ Скачать: /{link}\n\n'

    other_text = f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                 f'⬇ Скачать: /{link}\n\n'
    return first_text, other_text


def author_strings(count_books, author, link):
    link = link[1:].replace('/', '_', 1)
    operand = ':' if count_books < 50 else '>'

    first_text = f'🔎 Авторов по запросу найдено {operand} {count_books} 🔍\n\n\n' \
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
    operand = ':' if count_series < 50 else '>'

    first_text = f'🔎 Найдено совпадений {operand} {count_series} 🔍\n\n' \
                 f'📚<b>{series}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    other_text = f'📚<b>{series}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    return first_text, other_text


def series_book_strings(count_book, book, link):
    link = link[1:].replace('/', '_', 1)
    operand = ':' if count_book < 50 else '>'

    first_text = f'📚Найдено книг {operand} {count_book}\n\n' \
                 f'📖<b>{book}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    other_text = f'📖<b>{book}</b>\n' \
                 f'⬇Скачать: /{link}\n\n'

    return first_text, other_text


def no_result_message(method: str):
    text = ''
    if method == 'series':
        text = 'Ничего не найдено 😔\n' \
               'Возможно ты ввел неправильно название книжной серии\n\n' \
               'Например: \n' \
               '/series Властелин Колец\n' \
               '/series Плоский Мир'
    elif method == 'author':
        text = 'Ничего не найдено 😔\n' \
               'Возможно ты ввел неправильно ФИО автора\n\n' \
               'Например:\n' \
               '/author Достоевский\n' \
               '/author Стивен Кинг'
    elif method == 'book':
        text = 'По запросу ничего не найдено! 😔\n' \
               'Убедись правильно ли написано название книги\n\n' \
               f'{hlink(title="Как искать книги и ответы на частые вопросы", url="https://t.me/books_bar/66")}'
    return text


def message_into_bot(method: str):
    text = ''
    if method == 'series':
        text = f'Больше книжных серий доступно в группе -- @free_book_flibusta 📚\n' \
               f'Книжный бар: @books_bar 📚'
    elif method == 'author':
        text = f'Больше авторов доступно в группе -- @free_book_flibusta 📚\n' \
               f'Книжный бар: @books_bar 📚'

    elif method == 'book':
        text = f'Больше книг доступно в группе -- @free_book_flibusta 📚\n' \
               f'Книжный бар: @books_bar 📚'

    return text

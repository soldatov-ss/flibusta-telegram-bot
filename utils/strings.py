def book_strings(max_books, author, book, link):
    link = link[1:].replace('/', '_', 1)
    first_text = f'🔎  Найдено всего книг: {max_books}  🔍\n\n' \
                 f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                 f'⬇ Скачать: /{link}\n\n'

    other_text = f'📖 <b>{book}</b> -- <i>{author}</i> \n' \
                 f'⬇ Скачать: /{link}\n\n'

    return first_text, other_text


def author_strings(max_books, author, link):
    link = link[1:].replace('/', '_', 1)
    first_text = f'🔎 Авторов по запросу найдено: {max_books} 🔍\n\n\n' \
                 f'<b>{author}</b>\n' \
                 f'Книги автора: 📚/{link}\n\n'

    other_text = f'<b>{author}</b>\n' \
                 f'Книги автора: 📚/{link}\n\n'

    return first_text, other_text


def author_books(book, link):
    link = link[1:].replace('/', '_', 1)

    text = f'📖<b>{book}</b>\n' \
           f'⬇Скачать книгу: /{link}\n\n'

    return text

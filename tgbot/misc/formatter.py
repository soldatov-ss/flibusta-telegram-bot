def book_formatter(count: int, authors: str, book: str, link: str, is_first_page: bool) -> str:
    link = link[1:].replace('/', '_', 1)

    if is_first_page:
        text_page = f'🔎 Found {count} books total 🔍\n\n' \
                    f'📖 <b>{book}</b>\n' \
                    f'<i>{authors}</i>\n' \
                    f'⬇ Скачать: /{link}'
    else:
        text_page = f'📖 <b>{book}</b>\n' \
                    f'<i>{authors}</i>\n' \
                    f'⬇ Download: /{link}'
    return text_page

from infrastructure.dtos.author_dtos import AuthorBaseDTO
from infrastructure.dtos.book_dtos import BookFullInfoDTO, BooksDTO
from infrastructure.dtos.sequence_dtos import SequenceDTO
from tgbot.misc.book_utils import clean_html


def format_link(link: str) -> str:
    """Format the link for use in messages."""
    return link[1:].replace("/", "_", 1)


def book_formatter(count: int, authors: str, book: BooksDTO, link: str, is_first_page: bool) -> str:
    link = format_link(link)

    title_line = f"📖 <b>{book.title}</b> - <i>{book.lang}</i>"
    author_line = f"<i>{authors}</i>"
    download_line = f"⬇ Download: /{link}"

    if is_first_page:
        return f"🔎 Found {count} books total 🔍\n\n{title_line}\n{author_line}\n{download_line}"
    else:
        return f"{title_line}\n{author_line}\n{download_line}"


def book_by_author_formatter(count: int, author: str, book: BooksDTO, link: str, is_first_page: bool) -> str:
    link = format_link(link)

    title_line = f"📖 <b>{book.title}</b> - <i>{book.lang}</i>"
    download_line = f"⬇ Download: /{link}"

    if is_first_page:
        return f"🔎 Found {count} books total 🔍\n<b>{author}</b>\n\n{title_line}\n{download_line}"
    else:
        return f"{title_line}\n{download_line}"


def detailed_book_formatter(book: BookFullInfoDTO) -> str:
    description = clean_html(book.body) if book.body else "No description available."
    return (
        f"📖 <b>{book.title}</b>\n"
        f"<i>{book.authors}</i>\n"
        f"{book.sequences} \n"
        f"<i>{book.genres}</i>\n\n"
        f"{description}"[:4095]
    )


def author_formatter(count: int, author: AuthorBaseDTO, link: str, is_first_page: bool) -> str:
    link = format_link(link)

    author_name = f"{author.first_name} {author.middle_name.strip() if author.middle_name else ''} {author.last_name}"
    author_line = f"<b>{author_name}</b>"
    books_line = f"📚Author's books: /{link}"

    if is_first_page:
        return f"🔎 Found {count} authors total 🔍\n\n{author_line}\n{books_line}"
    else:
        return f"{author_line}\n{books_line}"


def sequence_formatter(count: int, sequence: SequenceDTO, link: str, is_first_page: bool) -> str:
    link = format_link(link)

    sequence_line = f"<b>📚{sequence.seq_name}</b>"
    author_line = f"Author: {sequence.seq_author_name}"
    books_line = f"Books: /{link}"

    if is_first_page:
        return f"🔎 Found {count} sequences total 🔍\n\n{sequence_line}\n{author_line}\n{books_line}"
    else:
        return f"{sequence_line}\n{author_line}\n{books_line}"


def books_by_sequence_formatter(count: int, author: str, sequence_name: str, book: BooksDTO, link: str,
                                is_first_page: bool) -> str:
    link = format_link(link)

    title_line = f"📚 <b>{sequence_name}</b>"
    author_line = f"<i>{author}</i>"
    book_line = f"📖 <b>{book.title}</b> - <i>{book.lang}</i>"
    download_line = f"⬇ Download: /{link}"

    if is_first_page:
        return f"🔎 Found {count} books total 🔍\n\n{title_line}\n{author_line}\n\n{book_line}\n{download_line}"
    else:
        return f"{book_line}\n{download_line}"

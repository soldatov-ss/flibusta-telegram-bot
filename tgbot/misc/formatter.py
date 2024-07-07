from infrastructure.dtos.author_dtos import AuthorBaseDTO
from infrastructure.dtos.book_dtos import BooksDTO


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


def author_formatter(count: int, author: AuthorBaseDTO, link: str, is_first_page: bool) -> str:
    link = format_link(link)

    author_name = f"{author.first_name} {author.middle_name.strip() if author.middle_name else ''} {author.last_name}"
    author_line = f"<b>{author_name}</b>"
    books_line = f"📚Author's books: /{link}"

    if is_first_page:
        return f"🔎 Found {count} authors total 🔍\n\n{author_line}\n{books_line}"
    else:
        return f"{author_line}\n{books_line}"

import logging
import re
import unicodedata

from aiogram.types import URLInputFile
from bs4 import BeautifulSoup

from infrastructure.dtos.book_dtos import BookFullInfoDTO
from infrastructure.enums.book_enums import DefaultBookFileFormats

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def book_name_to_filename(book_name):
    """
    Transform a book name into a valid filename by removing special characters, spaces,
    and normalizing the text.

    Args:
    - book_name (str): The name of the book to be transformed into a filename.

    Returns:
    - str: A string that is a valid filename.
    """
    normalized_name = unicodedata.normalize("NFKD", book_name)
    name_without_diacritics = "".join(c for c in normalized_name if not unicodedata.combining(c))

    cleaned_name = re.sub(r"[^\w\s-]", "", name_without_diacritics)
    cleaned_name = re.sub(r"[-\s]+", "_", cleaned_name).strip("_")

    return cleaned_name


async def get_book_file(book: BookFullInfoDTO, file_format: str):
    file_name = book.file_name or book_name_to_filename(book.title)

    if file_format not in DefaultBookFileFormats.list():
        format_to_download = "download"
    else:
        file_name = f"{file_name}.{file_format}"
        format_to_download = file_format

    url = f"https://flibusta.is/b/{book.book_id}/{format_to_download}"
    book = URLInputFile(url, filename=file_name)
    return book


def is_file_size_valid(file_size: int) -> bool:
    """
    Check if the file size is within the allowed limit.
    :param file_size: Size of the file in bytes
    :return: True if the file size is valid, False otherwise
    """
    return file_size <= MAX_FILE_SIZE


def clean_html(raw_html):
    """
    Cleans the given HTML content by removing all links and custom 'collapse' sections.

    :param raw_html: The raw HTML content to clean.
    :return: Cleaned text without HTML tags, links, and 'collapse' sections.
    """
    soup = BeautifulSoup(raw_html, "lxml")

    # Remove all links
    for a in soup.find_all("a"):
        a.decompose()

    cleantext = soup.get_text(separator=" ")
    cleantext = re.sub(r"\[collapse collapsed.*?\[/collapse\]", "", cleantext, flags=re.DOTALL)

    return cleantext

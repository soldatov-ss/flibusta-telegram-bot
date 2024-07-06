from datetime import datetime

from pydantic import BaseModel


class BookInfoDTO(BaseModel):
    book_id: int
    file_size: int
    time: datetime
    title: str
    title_1: str
    lang: str
    lang_ex: int
    src_lang: str
    file_type: str
    encoding: str
    year: int
    deleted: str
    ver: str
    file_author: str
    n: int
    keywords: str
    md_5: str
    modified: datetime
    pmd_5: str
    info_code: int
    pages: int
    chars: int
    average_rating: float | None = 0.0
    file_name: str | None = None


class BooksDTO(BookInfoDTO):
    authors: list[str] | None = []


class BookFullInfoDTO(BookInfoDTO):
    authors: str | None
    sequences: str | None
    genres: str | None
    average_rating: float | None = 0.0
    file_name: str | None = None
    body: str | None = None

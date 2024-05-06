from datetime import datetime
from typing import Optional, List

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
    average_rating: Optional[float] = 0.0
    file_name: Optional[str] = None


class BooksDTO(BookInfoDTO):
    authors: Optional[List[str]] = []


class BookFullInfoDTO(BookInfoDTO):
    authors: Optional[str] = []
    sequences: Optional[str] = []
    genres: Optional[str] = []
    average_rating: Optional[float] = 0.0
    file_name: Optional[str] = None
    body: Optional[str] = None

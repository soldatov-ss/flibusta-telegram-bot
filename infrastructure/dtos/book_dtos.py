from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from infrastructure.dtos.author_dtos import AuthorInfoDTO
from infrastructure.dtos.genre_dtos import GenreInfoDTO
from infrastructure.dtos.sequence_dtos import SequenceInfoDTO


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
    average_rating: float = 0.0
    file_name: Optional[str] = None


class BooksDTO(BookInfoDTO):
    authors: Optional[List[str]] = []


class BookFullInfoDTO(BookInfoDTO):
    authors: Optional[List[AuthorInfoDTO]] = []
    sequences: Optional[List[SequenceInfoDTO]] = []
    genres: Optional[List[GenreInfoDTO]] = []

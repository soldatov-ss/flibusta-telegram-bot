from pydantic import BaseModel


class GenreInfoDTO(BaseModel):
    book_id: int
    genre_id: int
    genre_code: str
    genre_desc: str
    genre_meta: str

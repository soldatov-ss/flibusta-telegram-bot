from pydantic import BaseModel


class AuthorInfoDTO(BaseModel):
    book_id: int
    author_id: int
    pos: int
    first_name: str
    middle_name: str
    last_name: str
    nick_name: str
    uid: int
    email: str
    homepage: str
    gender: str
    master_id: int

from pydantic import BaseModel


class AuthorBaseDTO(BaseModel):
    author_id: int
    first_name: str
    middle_name: str
    last_name: str
    nick_name: str
    uid: int
    email: str
    homepage: str
    gender: str
    master_id: int


class AuthorInfoDTO(AuthorBaseDTO):
    book_id: int
    pos: int

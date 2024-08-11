from pydantic import BaseModel


class SequenceInfoDTO(BaseModel):
    book_id: int
    seq_id: int
    seq_numb: int
    level: int
    type: bool
    seq_name: str


class SequenceDTO(BaseModel):
    seq_id: int
    seq_name: str
    seq_author_name: str

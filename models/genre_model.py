from sqlalchemy import Column, Integer

from models.base_model import BaseModel


class GenreModel(BaseModel):
    __tablename__ = 'libgenre'

    book_id = Column('BookId', Integer, nullable=False)
    genre_id = Column('GenreId', Integer, nullable=False)

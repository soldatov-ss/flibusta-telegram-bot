from sqlalchemy import Column, Integer

from .base import Base


class GenreModel(Base):
    __tablename__ = 'libgenre'

    book_id = Column('BookId', Integer, primary_key=True, nullable=False)
    genre_id = Column('GenreId', Integer, primary_key=True, nullable=False)

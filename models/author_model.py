from sqlalchemy import Column, Integer

from models.base_model import BaseModel


class AuthorModel(BaseModel):
    __tablename__ = 'libavtor'

    book_id = Column('BookId', Integer, primary_key=True)
    author_id = Column('AvtorId', Integer, primary_key=True)
    pos = Column('Pos', Integer)

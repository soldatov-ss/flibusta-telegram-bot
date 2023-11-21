from sqlalchemy import Column, Integer, String

from models.base_model import BaseModel


class BookRateModel(BaseModel):
    __tablename__ = 'librate'

    book_id = Column('BookId', Integer, nullable=False, unique=True)
    user_id = Column('UserId', Integer, nullable=False, unique=True)
    rate = Column('Rate', String(1), nullable=False)

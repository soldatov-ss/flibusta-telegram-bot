from sqlalchemy import Column, Integer, String

from .base import Base


class BookRateModel(Base):
    __tablename__ = 'librate'

    book_id = Column('BookId', Integer, primary_key=True, nullable=False, unique=True)
    user_id = Column('UserId', Integer, primary_key=True, nullable=False, unique=True)
    rate = Column('Rate', String(1), nullable=False)

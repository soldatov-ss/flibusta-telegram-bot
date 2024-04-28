from sqlalchemy import Column, Integer, String

from .base import Base


class FileNameModel(Base):
    __tablename__ = 'libfilename'

    book_id = Column('BookId', Integer, primary_key=True)
    file_name = Column('FileName', String(255), unique=True, nullable=False)

from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel


class FileNameModel(BaseModel):
    __tablename__ = 'libfilename'

    book_id = Column('BookId', Integer, primary_key=True)
    file_name = Column('FileName', String(255), unique=True, nullable=False)

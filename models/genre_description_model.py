from sqlalchemy import Column, Integer, String

from models.base_model import BaseModel


class GenreDescriptionModel(BaseModel):
    __tablename__ = 'libgenrelist'

    genre_id = Column('GenreId', Integer, primary_key=True, autoincrement=True)
    genre_code = Column('GenreCode', String(45), nullable=False, default='')
    genre_desc = Column('GenreDesc', String(99), nullable=False, default='')
    genre_meta = Column('GenreMeta', String(45), nullable=False, default='')

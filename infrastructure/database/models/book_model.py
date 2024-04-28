from sqlalchemy import Column, Integer, String, DateTime

from .base import Base


class BookModel(Base):
    __tablename__ = 'libbook'

    book_id = Column('BookId', Integer, primary_key=True)
    file_size = Column('FileSize', Integer, nullable=False, default=0)
    time = Column('Time', DateTime, nullable=False)
    title = Column('Title', String(254), nullable=False, default='')
    title_1 = Column('Title1', String(254), nullable=False)
    lang = Column('Lang', String(3), nullable=False, default='ru')
    lang_ex = Column('LangEx', Integer, nullable=False, default=0)
    src_lang = Column('SrcLang', String(3), nullable=False)
    file_type = Column('FileType', String(4), nullable=False)
    encoding = Column('Encoding', String(32), nullable=False, default='')
    year = Column('Year', Integer, nullable=False, default=0)
    deleted = Column('Deleted', String(1), nullable=False)
    ver = Column('Ver', String(8), nullable=False, default='')
    file_author = Column('FileAuthor', String(64), nullable=False)
    n = Column('N', Integer, nullable=False, default=0)
    keywords = Column('keywords', String(255), nullable=False)
    md_5 = Column('md5', String(32), unique=True, nullable=False)
    modified = Column('Modified', DateTime, nullable=False)
    pmd_5 = Column('pmd5', String(32), nullable=False, default='')
    info_code = Column('InfoCode', Integer, nullable=False, default=0)
    pages = Column('Pages', Integer, nullable=False, default=0)
    chars = Column('Chars', Integer, nullable=False, default=0)

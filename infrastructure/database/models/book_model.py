from sqlalchemy import Column, DateTime, Index, Integer, SmallInteger, String, UniqueConstraint

from .base import Base


class BookModel(Base):
    __tablename__ = "libbook"

    book_id = Column("BookId", Integer, primary_key=True, autoincrement=True, nullable=False)
    file_size = Column("FileSize", Integer, nullable=False, default=0)
    time = Column("Time", DateTime, nullable=False)
    title = Column("Title", String(254), nullable=False, default="")
    title_1 = Column("Title1", String(254), nullable=False)
    lang = Column("Lang", String(3), nullable=False, default="ru")
    lang_ex = Column("LangEx", SmallInteger, nullable=False, default=0)
    src_lang = Column("SrcLang", String(3), nullable=False, default="")
    file_type = Column("FileType", String(4), nullable=False)
    encoding = Column("Encoding", String(32), nullable=False, default="")
    year = Column("Year", SmallInteger, nullable=False, default=0)
    deleted = Column("Deleted", String(1), nullable=False, default="0")
    ver = Column("Ver", String(8), nullable=False, default="")
    file_author = Column("FileAuthor", String(64), nullable=False)
    n = Column("N", Integer, nullable=False, default=0)
    keywords = Column("keywords", String(255), nullable=False)
    md_5 = Column("md5", String(32), unique=True, nullable=False)
    modified = Column("Modified", DateTime, nullable=False, server_default="2009-11-29 05:00:00")
    pmd_5 = Column("pmd5", String(32), nullable=False, default="")
    info_code = Column("InfoCode", SmallInteger, nullable=False, default=0)
    pages = Column("Pages", Integer, nullable=False, default=0)
    chars = Column("Chars", Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("Deleted", "BookId", name="BookDel"),
        Index("Deleted", "Deleted"),
        Index("FileAuthor", "FileAuthor"),
        Index("FileSize", "FileSize"),
        Index("FileType", "FileType"),
        Index("Lang", "Lang"),
        Index("N", "N"),
        Index("Title", "Title"),
        Index("Title1", "Title1"),
        Index("Year", "Year"),
        {"mysql_collate": "utf8mb3_unicode_ci"},
    )

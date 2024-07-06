from sqlalchemy import Column, Integer, String, UniqueConstraint

from .base import Base


class FileNameModel(Base):
    __tablename__ = "libfilename"

    book_id = Column("BookId", Integer, primary_key=True, nullable=False)
    file_name = Column("FileName", String(255), unique=True, nullable=False)

    __table_args__ = (UniqueConstraint("FileName", name="file_name"), {"mysql_charset": "latin1"})

from sqlalchemy import Column, Index, Integer, SmallInteger

from .base import Base


class AuthorModel(Base):
    __tablename__ = "libavtor"

    book_id = Column("BookId", Integer, primary_key=True, nullable=False, default=0)
    author_id = Column("AvtorId", Integer, primary_key=True, nullable=False, default=0)
    pos = Column("Pos", SmallInteger, nullable=False, default=0)

    __table_args__ = (Index("iav", "AvtorId"),)

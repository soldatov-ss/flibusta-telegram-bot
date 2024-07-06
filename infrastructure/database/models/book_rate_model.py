from sqlalchemy import Column, Index, Integer, String, UniqueConstraint

from .base import Base


class BookRateModel(Base):
    __tablename__ = "librate"

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    book_id = Column("BookId", Integer, primary_key=True, nullable=False)
    user_id = Column("UserId", Integer, nullable=False)
    rate = Column("Rate", String(1), nullable=False)

    __table_args__ = (
        UniqueConstraint("BookId", "UserId", name="BookId_UserId"),
        Index("BookId", "BookId"),
        Index("UserId", "UserId"),
        {"mysql_charset": "latin1"},
    )

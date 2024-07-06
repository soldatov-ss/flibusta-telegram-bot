from sqlalchemy import Column, Index, Integer, UniqueConstraint

from .base import Base


class GenreModel(Base):
    __tablename__ = "libgenre"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    book_id = Column("BookId", Integer, nullable=False, default=0)
    genre_id = Column("GenreId", Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("BookId", "GenreId", name="u"),
        Index("ibook", "BookId"),
        Index("igenre", "GenreId"),
        {"mysql_collate": "utf8mb3_unicode_ci", "mysql_row_format": "DYNAMIC"},
    )

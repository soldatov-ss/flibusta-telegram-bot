from sqlalchemy import Column, Index, Integer, PrimaryKeyConstraint, String

from .base import Base


class GenreDescriptionModel(Base):
    __tablename__ = "libgenrelist"

    genre_id = Column("GenreId", Integer, primary_key=True, autoincrement=True)
    genre_code = Column("GenreCode", String(45), nullable=False, default="")
    genre_desc = Column("GenreDesc", String(99), nullable=False, default="")
    genre_meta = Column("GenreMeta", String(45), nullable=False, default="")

    __table_args__ = (
        PrimaryKeyConstraint("GenreId", "GenreCode"),
        Index("meta", "GenreMeta"),
        {"mysql_collate": "utf8mb3_unicode_ci"},
    )

from sqlalchemy import BIGINT, Column, ForeignKey, Integer, Table

from infrastructure.database.models import Base

book_user_association_table = Table(
    "book_user_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book_inner_info.book_id"), primary_key=True),
    Column("user_id", BIGINT, ForeignKey("users.user_id"), primary_key=True),
)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin
from .book_associations import book_user_association_table


class BookInnerInfoModel(Base, TimestampMixin):
    __tablename__ = "book_inner_info"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    book_id = Column(Integer, nullable=False, index=True)
    file_type = Column(String(25), nullable=False)
    file_id = Column(String(255), nullable=False, comment="Telegram file id")
    downloaded_by = relationship("User", secondary=book_user_association_table, back_populates="downloaded_books")

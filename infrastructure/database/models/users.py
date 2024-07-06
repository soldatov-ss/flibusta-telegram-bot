from typing import Optional

from sqlalchemy import String
from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .book_associations import book_user_association_table
from .base import Base, TimestampMixin, TableNameMixin


class User(Base, TimestampMixin, TableNameMixin):
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))

    downloaded_books = relationship(
        'BookInnerInfoModel',
        secondary=book_user_association_table,
        back_populates='downloaded_by'
    )

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.full_name}>"

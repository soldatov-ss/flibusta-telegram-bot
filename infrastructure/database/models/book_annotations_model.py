from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT

from infrastructure.database.models import Base


class BookAnnotationsModel(Base):
    __tablename__ = "libbannotations"

    book_id = Column("BookId", Integer, primary_key=True, nullable=False)
    nid = Column("nid", Integer, nullable=False)
    title = Column("Title", String(255), nullable=False)
    body = Column("Body", LONGTEXT, nullable=True)

    __table_args__ = {"mysql_collate": "utf8mb3_unicode_ci"}

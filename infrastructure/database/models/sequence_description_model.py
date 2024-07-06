from sqlalchemy import Boolean, Column, Index, Integer, PrimaryKeyConstraint, SmallInteger

from .base import Base


class SequenceDescriptionModel(Base):
    __tablename__ = "libseq"

    book_id = Column("BookId", Integer, nullable=False)
    seq_id = Column("SeqId", Integer, nullable=False)
    seq_numb = Column("SeqNumb", Integer, nullable=False)
    level = Column("Level", SmallInteger, nullable=False, default=0)
    type = Column("Type", Boolean, nullable=False, default=False)

    __table_args__ = (PrimaryKeyConstraint("BookId", "SeqId"), Index("SeqId", "SeqId"), {"mysql_charset": "latin1"})

from sqlalchemy import Column, Integer, Boolean, SmallInteger

from .base import Base


class SequenceDescriptionModel(Base):
    __tablename__ = 'libseq'

    book_id = Column('BookId', Integer, primary_key=True)
    seq_id = Column('SeqId', Integer, primary_key=True)
    seq_numb = Column('SeqNumb', Integer, nullable=False)
    level = Column('Level', SmallInteger, nullable=False, default=0)
    type = Column('Type', Boolean, nullable=False, default=False)

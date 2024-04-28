from sqlalchemy import Column, Integer, String

from .base import Base


class SequenceModel(Base):
    __tablename__ = 'libseqname'

    seq_id = Column('SeqId', Integer, primary_key=True, autoincrement=True)
    seq_name = Column('SeqName', String(254), nullable=False, unique=True, default='')

from sqlalchemy import Column, Integer, String

from models.base_model import BaseModel


class SequenceModel(BaseModel):
    __tablename__ = 'libseqname'

    seq_id = Column('SeqId', Integer, primary_key=True, autoincrement=True)
    seq_name = Column('SeqName', String(254), nullable=False, unique=True, default='')

from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel


class AuthorDescriptionModel(BaseModel):
    __tablename__ = 'libavtorname'

    author_id = Column('AvtorId', Integer, primary_key=True)
    first_name = Column('FirstName', String(99), nullable=False, default='')
    middle_name = Column('MiddleName', String(99), nullable=False, default='')
    last_name = Column('LastName', String(99), nullable=False, default='')
    nick_name = Column('NickName', String(33), nullable=False, default='')
    uid = Column('uid', Integer, nullable=False)
    email = Column('Email', String(255), nullable=False)
    homepage = Column('Homepage', String(255), nullable=False)
    gender = Column('Gender', String(1), nullable=False, default='')
    master_id = Column('MasterId', Integer)

from sqlalchemy import Column, Integer, String, BigInteger

from models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    user_id: int = Column(Integer, primary_key=True)
    full_name: str = Column(String(255), nullable=False)
    telegram_id: int = Column(BigInteger, nullable=False, unique=True)
    download_count: int = Column(BigInteger, default=0)

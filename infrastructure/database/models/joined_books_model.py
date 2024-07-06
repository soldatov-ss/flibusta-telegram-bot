from sqlalchemy import TIMESTAMP, Column, Index, Integer

from infrastructure.database.models import Base


class JoinedBooksModel(Base):
    __tablename__ = "libjoinedbooks"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    time = Column("Time", TIMESTAMP, nullable=False)
    bad_id = Column("BadId", Integer, nullable=False, default=0, unique=True)
    good_id = Column("GoodId", Integer, nullable=False, default=0)
    real_id = Column("realId", Integer, nullable=True)

    __table_args__ = (
        Index("GoodId", "GoodId"),
        Index("Time", "Time"),
        Index("realId", "realId"),
    )

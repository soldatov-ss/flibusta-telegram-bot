from sqlalchemy import Column, Index, Integer, String

from .base import Base


class AuthorDescriptionModel(Base):
    __tablename__ = "libavtorname"

    author_id = Column("AvtorId", Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column("FirstName", String(99), nullable=False, default="")
    middle_name = Column("MiddleName", String(99), nullable=False, default="")
    last_name = Column("LastName", String(99), nullable=False, default="")
    nick_name = Column("NickName", String(33), nullable=False, default="")
    uid = Column("uid", Integer, nullable=False, default=0)
    email = Column("Email", String(255), nullable=False)
    homepage = Column("Homepage", String(255), nullable=False)
    gender = Column("Gender", String(1), nullable=False, default="")
    master_id = Column("MasterId", Integer, nullable=False, default=0)

    __table_args__ = (
        Index("FirstName", "FirstName", mysql_length=20),
        Index("Homepage", "Homepage"),
        Index("LastName", "LastName", mysql_length=20),
        Index("MasterId", "MasterId"),
        Index("email", "Email"),
        Index("uid", "uid"),
    )

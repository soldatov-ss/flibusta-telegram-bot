from sqlalchemy import Column, Integer, String, UniqueConstraint

from .base import Base


class SequenceModel(Base):
    __tablename__ = "libseqname"

    seq_id = Column("SeqId", Integer, primary_key=True, autoincrement=True)
    seq_name = Column("SeqName", String(254), nullable=False, unique=True, default="")

    __table_args__ = (
        UniqueConstraint("SeqName", name="SeqName_2"),
        {
            "mysql_collate": "utf8mb3_unicode_ci",
            "mysql_comment": "Список форм (1-100) и названий сериа",
            "mysql_engine": "MyISAM",
        },
    )

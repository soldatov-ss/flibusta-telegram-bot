from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeMeta, registry, Mapped

mapper_registry = registry()


class Id(Integer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[Id] = Column(Id, primary_key=True)

    def __repr__(self):
        if self.id:
            return f'<{type(self)} with id {self.id}>'
        return super().__repr__()

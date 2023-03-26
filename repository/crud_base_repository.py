from typing import Generic, Type, TypeVar, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models.base_model import BaseModel, Id

ModelType = TypeVar("ModelType", bound=BaseModel)

url = 'mysql+aiomysql://mysql:password@172.22.0.2:3306/database'


class CRUDBaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model: Type[ModelType] = model
        self.engine = create_async_engine(url, echo=True)
        self.async_session = async_sessionmaker(self.engine, autoflush=True, expire_on_commit=False)

    async def create(self, model: ModelType) -> ModelType:
        async with self.async_session() as session:
            async with session.begin():
                session.add(model)
            await session.commit()
            await session.refresh(model)
        return model

    async def get_one(self, id: Id) -> Optional[ModelType]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(self.model).where(self.model.id == id))
                model = result.scalars().first()
        return model

    async def update(self, id: Id, model: ModelType):
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(self.model).where(self.model.id == id))
                obj = result.scalars().first()
                if obj:
                    for key, value in model.__dict__.items():
                        setattr(obj, key, value)
                await session.commit()
                await session.refresh(obj)

    async def delete(self, id: Id) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(self.model).where(self.model.id == id))
                obj = result.scalars().first()
                if obj:
                    await session.delete(obj)
                    await session.commit()
                    return True
                else:
                    return False

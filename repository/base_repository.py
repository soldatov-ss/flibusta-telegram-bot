from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

url = 'mysql+aiomysql://mysql:password@mysql:3306/database'

class CRUDBaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model: Type[ModelType] = model
        self.engine = create_async_engine(url, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)


from models import UserModel
from repository.crud_base_repository import CRUDBaseRepository


class UserRepository(CRUDBaseRepository[UserModel]):
    pass

user_repository = UserRepository(UserModel)

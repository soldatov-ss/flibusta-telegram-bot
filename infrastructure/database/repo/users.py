from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
            self,
            user_id: int,
            full_name: str,
            language: str,
            username: Optional[str] = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = insert(User).values(
            user_id=user_id,
            username=username,
            full_name=full_name,
            language=language
        ).on_duplicate_key_update(
            username=username,
            full_name=full_name,
            language=language
        )

        await self.session.execute(insert_stmt)
        await self.session.commit()

        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

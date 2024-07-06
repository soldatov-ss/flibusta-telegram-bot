import logging

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import selectinload

from infrastructure.database.models import BookInnerInfoModel, User
from infrastructure.database.repo.base import BaseRepo

logger = logging.getLogger(__name__)


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: str | None = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(user_id=user_id, username=username, full_name=full_name, language=language)
            .on_duplicate_key_update(username=username, full_name=full_name, language=language)
        )

        await self.session.execute(insert_stmt)
        await self.session.commit()

        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).options(selectinload(User.downloaded_books)).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def proceed_user_download_book(self, user_id: int, book_id: int, file_id: str, file_format: str) -> None:
        """
        Manages the downloading process for a book by a user, ensuring the book is registered
        as downloaded by the user in the database, or updates the existing record if it exists.
        """
        query = (
            select(BookInnerInfoModel)
            .options(selectinload(BookInnerInfoModel.downloaded_by))
            .where(BookInnerInfoModel.book_id == book_id, BookInnerInfoModel.file_type == file_format)
        )
        result = (await self.session.execute(query)).scalar_one_or_none()

        if result:
            logger.info("Book exists, updating file ID")
            result.file_id = file_id
            await self.session.commit()
        else:
            logger.info("Book does not exist, creating new record")
            with self.session.no_autoflush:
                result = BookInnerInfoModel(book_id=book_id, file_id=file_id, file_type=file_format)
                self.session.add(result)

                user = await self.get_user_by_id(user_id)
                if not user:
                    return
                if result.book_id not in {_.book_id for _ in user.downloaded_books}:
                    result.downloaded_by.append(user)
                await self.session.commit()

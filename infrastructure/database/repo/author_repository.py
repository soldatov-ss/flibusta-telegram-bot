from sqlalchemy import and_, exists, or_, select

from infrastructure.database.models import AuthorDescriptionModel, AuthorModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.author_dtos import AuthorBaseDTO, AuthorInfoDTO


class AuthorRepo(BaseRepo):
    async def get_authors_by_book_id(self, book_id: int) -> list[AuthorInfoDTO] | None:
        query = (
            select(AuthorModel, AuthorDescriptionModel)
            .join(AuthorDescriptionModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .where(AuthorModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        authors = result.all()
        if not authors:
            return []

        authors_info = [
            AuthorInfoDTO(book_id=author.book_id, pos=author.pos, **description.__dict__)
            for author, description in authors
        ]
        return authors_info

    async def get_authors_by_name(self, name: str) -> list[AuthorInfoDTO] | None:
        """
        Retrieves a list of authors based on a provided name, ensuring each author has associated books.

        This function processes the input name to handle scenarios where it might consist of either
        a full name (first and last), or just a single name part.
        """
        name_parts = name.split()
        if not name_parts:
            return []

        book_exists_subquery = (
            select(AuthorModel.author_id).where(AuthorModel.author_id == AuthorDescriptionModel.author_id).exists()
        )

        conditions = []
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            conditions.append(AuthorDescriptionModel.first_name.ilike(f"{first_name}%"))
            conditions.append(AuthorDescriptionModel.last_name.ilike(f"{last_name}%"))
        else:
            name = name_parts[0]
            conditions.append(
                or_(
                    AuthorDescriptionModel.first_name.ilike(f"{name}%"),
                    AuthorDescriptionModel.last_name.ilike(f"{name}%"),
                )
            )
        conditions.append(exists(book_exists_subquery))

        query = (
            select(AuthorDescriptionModel)
            .join(AuthorModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .where(and_(*conditions))
            .group_by(AuthorDescriptionModel.author_id)
        )

        result = await self.session.execute(query)
        authors = result.scalars().all()
        if not authors:
            return []

        authors_info = [AuthorBaseDTO(**description.__dict__) for description in authors]
        return authors_info

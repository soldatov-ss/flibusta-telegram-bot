
from sqlalchemy import select

from infrastructure.database.models import AuthorDescriptionModel, AuthorModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.author_dtos import AuthorInfoDTO


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

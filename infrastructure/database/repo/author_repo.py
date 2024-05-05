from typing import Optional, List

from sqlalchemy import select

from infrastructure.database.models import AuthorModel, AuthorDescriptionModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.author_dtos import AuthorInfoDTO


class AuthorRepo(BaseRepo):

    async def get_authors_by_book_id(self, book_id: int) -> Optional[List[AuthorInfoDTO]]:
        query = (
            select(AuthorModel, AuthorDescriptionModel)
            .join(AuthorDescriptionModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .where(AuthorModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        authors = result.all()
        if not authors:
            return []

        authors_info = [AuthorInfoDTO(
            book_id=author.book_id,
            author_id=author.author_id,
            pos=author.pos,
            first_name=description.first_name,
            middle_name=description.middle_name,
            last_name=description.last_name,
            nick_name=description.nick_name,
            uid=description.uid,
            email=description.email,
            homepage=description.homepage,
            gender=description.gender,
            master_id=description.master_id
        ) for author, description in authors]

        return authors_info

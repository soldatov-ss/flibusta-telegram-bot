from typing import Optional, List

from sqlalchemy import select

from infrastructure.database.models import GenreModel, GenreDescriptionModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.genre_dtos import GenreInfoDTO


class GenreRepo(BaseRepo):
    async def get_genres_by_book_id(self, book_id: int) -> Optional[List[GenreInfoDTO]]:
        query = (
            select(GenreModel, GenreDescriptionModel)
            .join(GenreDescriptionModel, GenreModel.genre_id == GenreDescriptionModel.genre_id)
            .where(GenreModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        genres = result.all()

        if not genres:
            return []

        return [GenreInfoDTO(
            book_id=genre.book_id,
            genre_id=genre.genre_id,
            genre_code=description.genre_code,
            genre_desc=description.genre_desc,
            genre_meta=description.genre_meta
        ) for genre, description in genres]

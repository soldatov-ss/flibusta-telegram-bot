from sqlalchemy import select, func

from infrastructure.database.models import BookModel, FileNameModel, BookRateModel, AuthorModel, AuthorDescriptionModel
from infrastructure.database.repo.base import BaseRepo


class BookRepo(BaseRepo):

    async def get_book_info_by_id(self, book_id: int):
        query = (
            select(
                BookModel,
                FileNameModel.file_name,
                func.avg(BookRateModel.rate).label("average_rating")
            )
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .outerjoin(FileNameModel, BookModel.book_id == FileNameModel.book_id)
            .where(BookModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        rows = result.all()

        if not rows:
            return None
        return rows

    async def get_books_with_authors_by_title(self, title: str):
        query = (
            select(
                BookModel,
                AuthorDescriptionModel,
                func.avg(BookRateModel.rate).label("average_rating")
            )
            .outerjoin(AuthorModel, BookModel.book_id == AuthorModel.book_id)
            .outerjoin(AuthorDescriptionModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .where(BookModel.title.ilike(f'%{title}%'))
            .group_by(BookModel.book_id, AuthorModel.author_id, AuthorDescriptionModel.author_id)
            .order_by(BookModel.title, func.avg(BookRateModel.rate).desc())
        )
        result = await self.session.execute(query)
        books = result.all()

        if not books:
            return []
        return books

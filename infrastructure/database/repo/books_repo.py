from sqlalchemy import select, func, not_

from infrastructure.database.models import BookModel, FileNameModel, BookRateModel, AuthorModel, AuthorDescriptionModel, \
    JoinedBooksModel
from infrastructure.database.models.book_annotations_model import BookAnnotationsModel
from infrastructure.database.repo.base import BaseRepo


class BookRepo(BaseRepo):

    async def get_book_info_by_id(self, book_id: int):
        query = (
            select(
                BookModel,
                FileNameModel.file_name,
                BookAnnotationsModel.body,
                func.avg(BookRateModel.rate).label("average_rating"),
            )
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .outerjoin(FileNameModel, BookModel.book_id == FileNameModel.book_id)
            .outerjoin(BookAnnotationsModel, BookModel.book_id == BookAnnotationsModel.book_id)
            .where(BookModel.book_id == book_id)
            .group_by(
                BookModel.book_id, FileNameModel.file_name, BookAnnotationsModel.body
            )
        )
        result = await self.session.execute(query)
        rows = result.all()

        if not rows:
            return None
        return rows[0]

    async def get_books_with_authors_by_title(self, title: str):
        # Subquery to get all bad_ids to exclude
        subquery_bad_ids = select(JoinedBooksModel.bad_id).subquery()

        query = (
            select(
                BookModel,
                AuthorDescriptionModel,
                func.avg(BookRateModel.rate).label("average_rating")
            )
            .outerjoin(AuthorModel, BookModel.book_id == AuthorModel.book_id)
            .outerjoin(AuthorDescriptionModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .where(
                BookModel.title.ilike(f'%{title}%'),
                not_(BookModel.book_id.in_(subquery_bad_ids))  # type: ignore
            )
            .group_by(BookModel.book_id, AuthorModel.author_id, AuthorDescriptionModel.author_id)
            .order_by(func.avg(BookRateModel.rate).desc(), BookModel.title)
        )
        result = await self.session.execute(query)
        books = result.all()

        if not books:
            return []
        return books

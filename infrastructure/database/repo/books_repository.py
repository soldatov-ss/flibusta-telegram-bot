from sqlalchemy import func, not_, select
from sqlalchemy.orm import aliased

from infrastructure.database.models import (
    AuthorDescriptionModel,
    AuthorModel,
    BookInnerInfoModel,
    BookModel,
    BookRateModel,
    FileNameModel,
    JoinedBooksModel,
    SequenceDescriptionModel,
    SequenceModel,
)
from infrastructure.database.models.book_annotations_model import BookAnnotationsModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.book_dtos import BookInfoDTO


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
            .group_by(BookModel.book_id, FileNameModel.file_name, BookAnnotationsModel.body)
        )
        result = await self.session.execute(query)
        rows = result.all()

        if not rows:
            return None
        return rows[0]

    async def get_books_with_authors_by_title(self, title: str) -> BookInnerInfoModel | list:
        # Subquery to get all bad_ids to exclude
        subquery_bad_ids = select(JoinedBooksModel.bad_id).subquery()

        query = (
            select(BookModel, AuthorDescriptionModel, func.avg(BookRateModel.rate).label("average_rating"))
            .outerjoin(AuthorModel, BookModel.book_id == AuthorModel.book_id)
            .outerjoin(AuthorDescriptionModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .where(
                BookModel.title.ilike(f"%{title}%"),
                not_(BookModel.book_id.in_(subquery_bad_ids)),  # type: ignore
            )
            .group_by(BookModel.book_id, AuthorModel.author_id, AuthorDescriptionModel.author_id)
            .order_by(func.avg(BookRateModel.rate).desc(), BookModel.title)
        )
        result = await self.session.execute(query)
        books = result.all()

        if not books:
            return []
        return books

    async def get_book_file_id(self, book_id: int, file_format: str) -> BookInnerInfoModel | None:
        query = select(BookInnerInfoModel).where(
            BookInnerInfoModel.book_id == book_id, BookInnerInfoModel.file_type == file_format
        )
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def get_books_by_author_id(self, author_id: int) -> list[BookInfoDTO] | list:
        # Subquery to get all bad_ids to exclude
        subquery_bad_ids = select(JoinedBooksModel.bad_id).subquery()

        query = (
            select(BookModel, AuthorDescriptionModel, func.avg(BookRateModel.rate).label("average_rating"))
            .outerjoin(AuthorModel, BookModel.book_id == AuthorModel.book_id)
            .outerjoin(AuthorDescriptionModel, AuthorModel.author_id == AuthorDescriptionModel.author_id)
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .where(
                AuthorModel.author_id == author_id,
                not_(BookModel.book_id.in_(subquery_bad_ids)),  # type: ignore
            )
            .group_by(BookModel.book_id, AuthorModel.author_id, AuthorDescriptionModel.author_id)
            .order_by(func.avg(BookRateModel.rate).desc(), BookModel.title)
        )
        result = await self.session.execute(query)
        books = result.all()
        if not books:
            return []
        return books

    async def get_books_by_sequence_id(self, seq_id: int):
        subquery_bad_ids = select(JoinedBooksModel.bad_id).subquery()

        SequenceAlias = aliased(SequenceModel)
        SequenceDescriptionAlias = aliased(SequenceDescriptionModel)
        AuthorAlias = aliased(AuthorModel)
        AuthorDescriptionAlias = aliased(AuthorDescriptionModel)

        query = (
            select(
                BookModel,
                AuthorDescriptionAlias,
                func.avg(BookRateModel.rate).label("average_rating"),
                SequenceAlias.seq_name
            )
            .outerjoin(SequenceDescriptionAlias, BookModel.book_id == SequenceDescriptionAlias.book_id)
            .outerjoin(SequenceAlias,
                       SequenceDescriptionAlias.seq_id == SequenceAlias.seq_id)
            .outerjoin(AuthorAlias, BookModel.book_id == AuthorAlias.book_id)
            .outerjoin(AuthorDescriptionAlias, AuthorAlias.author_id == AuthorDescriptionAlias.author_id)
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .where(
                SequenceDescriptionAlias.seq_id == seq_id,
                not_(BookModel.book_id.in_(subquery_bad_ids)),  # type: ignore
            )
            .group_by(BookModel.book_id, AuthorAlias.author_id, AuthorDescriptionAlias.author_id,
                      SequenceAlias.seq_name)
            .order_by(func.avg(BookRateModel.rate).desc(), BookModel.title)
        )

        result = await self.session.execute(query)
        books = result.all()
        if not books:
            return []
        
        return books

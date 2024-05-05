from typing import Optional, List

from sqlalchemy import select

from infrastructure.database.models import BookModel, FileNameModel, BookRateModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.book_dtos import BookInfoDTO


class BookRepo(BaseRepo):

    async def fetch_by_id(self, model, id: int):
        """
        Fetches a single entry from the database by book ID for the given model.
        :param model: The model class of the database table to query.
        :param id: The ID of the entry to fetch.
        :return: The fetched model instance or None if not found.
        """
        query = select(model).where(model.book_id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def fetch_many_by_id(self, model, id: int):
        """
        Fetches many entries from the database by book ID for the given model.
        :param model: The model class of the database table to query.
        :param id: The ID of the entry to fetch.
        :return: The fetched model instance or None if not found.
        """
        query = select(model).where(model.book_id == id)
        result = await self.session.execute(query)
        return result.all()

    async def get_book_by_id(self, book_id: int) -> Optional[BookModel]:
        """
        Fetches a book from the database by its ID.
        :param book_id: The book's ID.
        :return: BookModel object, or None if the book does not exist.
        """

        result = await self.fetch_by_id(BookModel, book_id)
        return result

    async def get_books_by_title(self, title: str):
        """
        Fetches books from the database where the title contains a given substring.
        :param title: Substring to search for in book titles.
        :return: List of BookModel objects that match the search criteria, or an empty list if no matches found.
        """
        query = select(BookModel).where(BookModel.title.ilike(f'%{title}%'))
        result = await self.session.execute(query)
        return result.all()

    async def get_book_info_by_id(self, book_id: int) -> Optional[BookInfoDTO]:
        query = (
            select(BookModel, BookRateModel, FileNameModel)
            .outerjoin(BookRateModel, BookModel.book_id == BookRateModel.book_id)
            .outerjoin(FileNameModel, BookModel.book_id == FileNameModel.book_id)
            .where(BookModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        rows = result.all()
        if not rows:
            return None

        book = rows[0][0]

        # Collect file name and all ratings
        rates = [row[1] for row in rows if row[1]]
        file_name = rows[0][2].file_name if rows[0][2] else None

        average_rating = self.calculate_average_rating(rates)

        book_info = BookInfoDTO(
            average_rating=average_rating,
            file_name=file_name,
            **book.__dict__,
        )

        return book_info

    @staticmethod
    def calculate_average_rating(rates: List[BookRateModel]) -> float:
        total_rate = sum(int(rate.rate) for rate in rates if rate.rate.isdigit())
        count_rate = len(rates)
        average_rating = total_rate / count_rate if count_rate > 0 else 0.0
        return round(average_rating, 2)

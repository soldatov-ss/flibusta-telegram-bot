from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import aliased

from infrastructure.database.models import BookModel, AuthorModel, BookRateModel, FileNameModel, GenreModel, \
    SequenceDescriptionModel
from infrastructure.database.repo.base import BaseRepo


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

    async def get_full_book_info(self, book_id: int):
        book = await self.fetch_by_id(BookModel, book_id)

        if not book:
            return None

        book_info = {
            "book": book,
            "authors": await self.fetch_many_by_id(AuthorModel, book_id),
            "ratings": await self.fetch_many_by_id(BookRateModel, book_id),
            "filenames": await self.fetch_many_by_id(FileNameModel, book_id),
            "genres": await self.fetch_many_by_id(GenreModel, book_id),
            "sequences": await self.fetch_many_by_id(SequenceDescriptionModel, book_id),
        }

        return book_info


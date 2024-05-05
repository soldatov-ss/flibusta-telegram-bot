from dataclasses import dataclass
from typing import Optional, List

from infrastructure.database.models import AuthorDescriptionModel
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.dtos.book_dtos import BookFullInfoDTO, BooksDTO, BookInfoDTO


@dataclass
class BookService(RequestsRepo):
    async def get_full_book_info(self, book_id: int) -> Optional[BookFullInfoDTO]:
        """
        Retrieves detailed information about a book including its authors, sequences, and genres.
        :param book_id: ID of the book to retrieve.
        :return: A DTO containing all detailed information of the book, or None if no book is found.
        """
        book_info = await self.books.get_book_info_by_id(book_id)
        if not book_info:
            return None

        authors = await self.authors.get_authors_by_book_id(book_id)
        sequences = await self.sequences.get_sequences_by_book_id(book_id)
        genres = await self.genres.get_genres_by_book_id(book_id)

        # Construct the full book info DTO
        full_book_info = BookFullInfoDTO(
            **book_info.model_dump(),
            authors=authors,
            sequences=sequences,
            genres=genres
        )
        return full_book_info

    async def get_books_with_authors_by_title(self, title: str) -> Optional[List[BooksDTO]]:
        """
        Searches for books by title and includes associated authors and their average ratings.
        :param title: The title substring to search for.
        :return: A list of books matching the title with author and rating details, or None if no matches found.
        """
        books = await self.books.get_books_with_authors_by_title(title.lower())
        if not books:
            return None

        books_dict = {}

        for book, description, average_rate in books:
            if book.book_id not in books_dict:
                books_dict[book.book_id] = {
                    **book.__dict__,
                    "average_rating": round(average_rate, 2) if average_rate else 0.0,
                    "authors": []
                }
            if description:
                full_name = self.get_author_full_name(description)
                books_dict[book.book_id]["authors"].append(full_name)

        books_with_authors = [BooksDTO(**data) for data in books_dict.values()]
        return books_with_authors

    async def get_book_info_by_id(self, book_id: int) -> Optional[BookInfoDTO]:
        """
        Retrieves basic information about a book by its ID.
        :param book_id: ID of the book to retrieve.
        :return: A DTO containing basic book information, or None if the book is not found.
        """
        result = await self.books.get_book_info_by_id(book_id)
        if not result:
            return None
        book, file_name, average_rating = result

        book_info = BookInfoDTO(
            average_rating=round(average_rating, 2) if average_rating else None,
            file_name=file_name or None,
            **book.__dict__,
        )
        return book_info

    @staticmethod
    def get_author_full_name(author: AuthorDescriptionModel) -> str:
        return f'{author.first_name} {author.middle_name} {author.last_name}'.strip()

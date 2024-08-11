from dataclasses import dataclass

from infrastructure.database.models import AuthorDescriptionModel
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.dtos.book_dtos import BookFullInfoDTO, BookInfoDTO, BooksDTO
from infrastructure.enums.book_enums import DefaultBookFileFormats
from tgbot.misc.book_utils import get_book_file


@dataclass
class BookService(RequestsRepo):
    async def get_full_book_info(self, book_id: int) -> BookFullInfoDTO | None:
        """
        Retrieves detailed information about a book including its authors, sequences, and genres.
        :param book_id: ID of the book to retrieve.
        :return: A DTO containing all detailed information of the book, or None if no book is found.
        """
        result = await self.books.get_book_info_by_id(book_id)
        if not result:
            return None

        book, file_name, body, average_rating = result

        # Gather additional details
        authors = await self.gather_authors(book_id)
        sequences = await self.gather_sequences(book_id)
        genres = await self.gather_genres(book_id)

        # Construct the full book info DTO
        full_book_info = BookFullInfoDTO(
            **book.__dict__,
            authors=", ".join(authors),
            sequences=", ".join(sequences),
            genres=", ".join(genres),
            average_rating=round(average_rating, 2) if average_rating else None,
            file_name=file_name or None,
            body=body or None,
        )
        return full_book_info

    async def get_books_with_authors_by_title(self, title: str) -> list[BooksDTO] | None:
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
                    "authors": [],
                }
            if description:
                full_name = self.get_author_full_name(description)
                books_dict[book.book_id]["authors"].append(full_name)

        books_with_authors = [BooksDTO(**data) for data in books_dict.values()]
        return books_with_authors

    async def get_books_by_author(self, author_id: int) -> tuple[list[BookInfoDTO], str] | None:
        books = await self.books.get_books_by_author_id(author_id)
        if not books:
            return None

        author = None
        books_dict = {}

        for book, description, average_rate in books:
            if book.book_id not in books_dict:
                books_dict[book.book_id] = {
                    **book.__dict__,
                    "average_rating": round(average_rate, 2) if average_rate else 0.0,
                }
            if description and author is None:
                author = self.get_author_full_name(description)

        books_by_author = [BookInfoDTO(**data) for data in books_dict.values()]
        return books_by_author, author

    async def get_books_by_sequence(self, seq_id: int) -> tuple[str, list[BookInfoDTO], str] | None:
        books = await self.books.get_books_by_sequence_id(seq_id)
        if not books:
            return None

        books_dict = {}
        sequence_name, author = None, None

        for book, author_description, average_rate, seq_name in books:
            sequence_name = seq_name
            author = self.get_author_full_name(author_description)

            if book.book_id not in books_dict:
                books_dict[book.book_id] = {
                    **book.__dict__,
                    "average_rating": round(average_rate, 2) if average_rate else 0.0,
                }

        books_by_sequence = [BookInfoDTO(**data) for data in books_dict.values()]
        return sequence_name, books_by_sequence, author

    async def gather_authors(self, book_id: int) -> list[str] | None:
        authors = await self.authors.get_authors_by_book_id(book_id)
        if not authors:
            return []
        return [f"{author.first_name} {author.middle_name} {author.last_name}".strip() for author in authors]

    async def gather_sequences(self, book_id: int) -> list[str] | None:
        sequences = await self.sequences.get_sequence_by_book_id(book_id)
        return [item.seq_name.strip() for item in sequences if sequences]

    async def gather_genres(self, book_id: int) -> list[str] | None:
        genres = await self.genres.get_genres_by_book_id(book_id)
        return [genre.genre_desc.strip() for genre in genres if genres]

    @staticmethod
    def get_author_full_name(author: AuthorDescriptionModel) -> str:
        return f"{author.first_name} {author.middle_name} {author.last_name}".strip()

    @staticmethod
    def get_book_file_formats(book: BookFullInfoDTO):
        if book.file_name:
            return [book.file_name.split(".")[-1].lower()]
        return DefaultBookFileFormats.list()

    async def get_book_file_id(self, book: BookFullInfoDTO, file_format: str):
        inner_book = await self.books.get_book_file_id(book.book_id, file_format)
        if not inner_book:
            return await get_book_file(book, file_format)
        return inner_book.file_id

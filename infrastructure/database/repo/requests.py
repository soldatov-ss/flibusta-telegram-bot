from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.author_repo import AuthorRepo
from infrastructure.database.repo.books_repo import BookRepo
from infrastructure.database.repo.genres_repo import GenreRepo
from infrastructure.database.repo.sequence_repo import SequenceRepo
from infrastructure.database.repo.users import UserRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.session)

    @property
    def books(self) -> BookRepo:
        """
        The BookRepo repository sessions are required to manage books operations.
        """
        return BookRepo(self.session)

    @property
    def authors(self) -> AuthorRepo:
        """
        The AuthorRepo repository sessions are required to manage author operations.
        """
        return AuthorRepo(self.session)

    @property
    def sequences(self) -> SequenceRepo:
        """
        The SequenceRepo repository sessions are required to manage sequence operations.
        """
        return SequenceRepo(self.session)

    @property
    def genres(self) -> GenreRepo:
        """
        The GenreRepo repository sessions are required to manage genres operations.
        """
        return GenreRepo(self.session)

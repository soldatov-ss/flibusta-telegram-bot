from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.author_repository import AuthorRepo
from infrastructure.database.repo.books_repository import BookRepo
from infrastructure.database.repo.genres_repository import GenreRepo
from infrastructure.database.repo.sequence_repository import SequencesRepo
from infrastructure.database.repo.user_repository import UserRepo


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
    def sequences(self) -> SequencesRepo:
        """
        The SequencesRepo repository sessions are required to manage book series operations.
        """
        return SequencesRepo(self.session)

    @property
    def genres(self) -> GenreRepo:
        """
        The GenreRepo repository sessions are required to manage genres operations.
        """
        return GenreRepo(self.session)

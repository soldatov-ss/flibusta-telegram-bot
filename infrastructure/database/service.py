from contextlib import asynccontextmanager

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import session_pool


@asynccontextmanager
async def get_repository():
    async with session_pool() as session:
        repo = RequestsRepo(session)
        try:
            yield repo
        finally:
            await session.commit()

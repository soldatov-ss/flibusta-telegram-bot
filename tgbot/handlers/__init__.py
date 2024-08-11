"""Import all routers and add them to routers_list."""

from .admin import admin_router
from .authors import author_router
from .books import books_router
from .sequences import sequence_router
from .user import user_router

routers_list = [
    admin_router,
    user_router,
    author_router,
    sequence_router,
    books_router,
]

__all__ = [
    "routers_list",
]

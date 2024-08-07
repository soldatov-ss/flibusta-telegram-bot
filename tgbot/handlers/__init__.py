"""Import all routers and add them to routers_list."""

from .admin import admin_router
from .authors import author_router
from .books import books_router
from .echo import echo_router

# from .simple_menu import menu_router
from .user import user_router

routers_list = [
    admin_router,
    # menu_router,
    user_router,
    author_router,
    # echo_router,  # echo_router must be last
    books_router,
]

__all__ = [
    "routers_list",
]

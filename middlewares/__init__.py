from loader import dp
from .antispam import CheckTypeMessage
from .throttling import ThrottlingMiddleware

if __name__ == 'middlewares':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckTypeMessage())

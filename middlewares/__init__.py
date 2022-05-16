from integrations.telegraph import TelegraphService
from loader import dp
from .antispam import CheckTypeMessage
from .integration import IntegrationMiddleware
from .throttling import ThrottlingMiddleware

if __name__ == 'middlewares':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckTypeMessage())
    file_uploader = TelegraphService()
    dp.middleware.setup(IntegrationMiddleware(file_uploader))
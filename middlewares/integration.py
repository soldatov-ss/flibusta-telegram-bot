from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject

from integrations.telegraph import FileUploader


class IntegrationMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, uploader: FileUploader):
        super().__init__()
        self._uploader = uploader

    async def pre_process(self, obj: TelegramObject, data: Dict[Any, Any], *args: Any):
        data["file_uploader"] = self._uploader
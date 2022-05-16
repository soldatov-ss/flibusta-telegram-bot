import abc

from aiogram.types import PhotoSize

from integrations.telegraph.types import UploadedFile


class FileUploader(abc.ABC):

    async def upload_photo(self, photo: PhotoSize) -> UploadedFile:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

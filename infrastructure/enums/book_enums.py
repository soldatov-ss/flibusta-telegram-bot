from enum import StrEnum, auto


class ExtendedEnum(StrEnum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class DefaultBookFileFormats(ExtendedEnum):
    FB2 = auto()
    EPUB = auto()
    MOBI = auto()

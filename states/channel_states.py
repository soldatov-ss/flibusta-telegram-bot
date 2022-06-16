from aiogram.dispatcher.filters.state import StatesGroup, State


class Post(StatesGroup):
    Image = State()
    Book = State()
    Author = State()
    Description = State()
    RuLink = State()
    UaLink = State()

class UpgradePost(StatesGroup):
    Post = State()


import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

user_router = Router()
logger = logging.getLogger(__name__)


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Вітаю, звичайний користувач!")

from aiogram import types
from aiogram.types import BotCommandScopeChat


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запуск бота"),
            types.BotCommand("author", "Поиск книг по автору"),
            types.BotCommand("series", "Поиск книг по названию серии"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("rating_b", "топ 10 книг"),
            types.BotCommand("rating_a", "топ 10 авторов")
        ]
    )


async def set_admin_commands(dp, chat_id):
    # Комманды для админа в боте
    await dp.bot.set_my_commands(
        [
            types.BotCommand("rating_user", "Кол-во пользователей"),
            types.BotCommand("rating_book", "Кол-во скачанных книг"),
            types.BotCommand("author", "Поиск книг по автору"),
            types.BotCommand("series", "Поиск книг по названию серии"),
            types.BotCommand("rating_b", "топ 10 книг"),
            types.BotCommand("rating_a", "топ 10 авторов"),
            types.BotCommand("start", "Запуск бота"),
            types.BotCommand("help", "Вывести справку"),

        ],
        scope=BotCommandScopeChat(chat_id=chat_id)
    )


from aiogram.types import BotCommandScopeChat, BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand("start", "Запуск бота"),
            BotCommand("author", "Поиск книг по автору"),
            BotCommand("series", "Поиск книг по названию серии"),
            BotCommand("help", "Вывести справку"),
            BotCommand("rating_b", "топ 10 книг"),
            BotCommand("rating_a", "топ 10 авторов")
        ]
    )


async def set_admin_commands(dp, chat_id):
    # Комманды для админа в боте
    await dp.bot.set_my_commands(
        [
            BotCommand("rating_user", "Кол-во пользователей"),
            BotCommand("rating_book", "Кол-во скачанных книг"),
            BotCommand("log_file", "Получить файл с логгами"),
            BotCommand("author", "Поиск книг по автору"),
            BotCommand("series", "Поиск книг по названию серии"),
            BotCommand("rating_b", "топ 10 книг"),
            BotCommand("rating_u", "топ 10 юзеров"),
            BotCommand("rating_a", "топ 10 авторов"),
            BotCommand("start", "Запуск бота"),
            BotCommand("help", "Вывести справку"),

        ],
        scope=BotCommandScopeChat(chat_id=chat_id)
    )

async def set_group_commands(dp, group_id):
    await dp.bot.set_my_commands(
        [
            BotCommand("start", "Запуск бота"),
            BotCommand("author", "Поиск книг по автору"),
            BotCommand("series", "Поиск книг по названию серии"),
            BotCommand("help", "Вывести справку"),
            BotCommand("rating_b", "топ 10 книг"),
            BotCommand("rating_a", "топ 10 авторов"),
            BotCommand("report", "Пожаловаться на спам/рекламу/пользователя"),
        ],
        scope=BotCommandScopeChat(chat_id=group_id)
    )

from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запуск бота"),
            types.BotCommand("author", "Поиск книг по автору"),
            types.BotCommand("series", "Поиск книг по названию серии"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("rating", "топ 10 книг")
        ]
    )

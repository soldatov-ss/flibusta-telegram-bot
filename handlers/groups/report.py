import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink

from filters import IsReplyFilter, IsGroup
from keyboards.inline.admin import report_reactions_keyboard, report_cb
from loader import dp, bot
from utils.throttlig import rate_limit


@rate_limit(limit=3)
@dp.message_handler(IsGroup(), IsReplyFilter(True), Command("report", prefixes={"/", "!"}))
async def report_user(message: types.Message):
    """Отправляет жалобу на пользователя админам"""

    reply = message.reply_to_message

    # Проверка на то что реплай сообщение написано от имени канала
    if reply.sender_chat:
        mention = reply.sender_chat.title
    else:
        mention = reply.from_user.get_mention()

    await message.answer(
        f"Репорт на пользователя {mention} успешно отправлен.\n"
        "Администрация предпримет все необходимые меры"
    )

    chat_admins = await bot.get_chat_administrators(message.chat.id)

    for admin in chat_admins:
        admin_id = admin.user.id

        if not admin.user.is_bot:
            await dp.bot.send_message(
                chat_id=admin_id,
                text=f"Кинут репорт на пользователя {mention} "
                     "за следующее " + hlink("сообщение", message.reply_to_message.url),
                reply_markup=report_reactions_keyboard(
                    message.reply_to_message.from_user.id,
                    message.reply_to_message.chat.id,
                    message.reply_to_message.message_id)
            )
            await asyncio.sleep(0.05)


@dp.message_handler(IsGroup(), Command("report", prefixes={"/", "!"}))
async def report_user_if_command_is_not_reply(message: types.Message):
    """Уведомляет, что репорт должен быть ответом"""
    await message.reply(
        "Сообщение с командой должно быть ответом на сообщение пользователя, "
        "на которого вы хотите пожаловаться"
    )



@dp.callback_query_handler(report_cb.filter())
async def report_user_callback(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get('action')
    message_id = callback_data.get('message_id')
    user_id = callback_data.get('user_id')
    chat_id = callback_data.get('chat_id')
    try:
        if action == 'ban':
            await call.bot.kick_chat_member(
                chat_id, user_id, revoke_messages=False
            )
            await call.bot.delete_message(chat_id, message_id)
        elif action == 'ban_delete':
            await call.bot.kick_chat_member(
                chat_id, user_id, revoke_messages=True
            )
        elif action == 'delete':
            await call.bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass
    finally:
        await call.message.delete_reply_markup()

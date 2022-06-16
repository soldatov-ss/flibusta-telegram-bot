import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from filters import IsBot
from handlers.users.find_authors import author_command
from handlers.users.find_books import find_books
from handlers.users.find_series import series_command
from keyboards.inline.admin import report_reactions_keyboard
from keyboards.inline.other_keyboards import get_requests, result_request
from loader import dp, bot
from utils.parsing.other import create_list_choices
from utils.throttlig import rate_limit


@rate_limit(limit=3)
@dp.message_handler(IsBot())
async def main_handler(message: types.Message, state: FSMContext):
    '''
    Принимает запрос от юзера и выводит клавиатуру, с доступными вариантами (книги автора, книги, серии)
    '''
    if message.reply_to_message: return
    if await spam_checking(message): return

    choice_buttons = await create_list_choices(message)
    if not choice_buttons:
        return
    elif len(choice_buttons) > 1:
        text = '💡Найдены следующие результаты💡\n' \
               'Чтобы продолжить сделай свой выбор 👇'
        await message.answer(text,
                             reply_markup=get_requests(req_lst=choice_buttons))

        async with state.proxy() as data:
            data["info"] = message

    elif choice_buttons[0] == 'Книжные серии':
        await series_command(message)
    elif choice_buttons[0] == 'Книги':
        await find_books(message)
    elif choice_buttons[0] == 'Писатели':
        await author_command(message)


@rate_limit(limit=3)
@dp.callback_query_handler(result_request.filter())
async def current_result(call: types.CallbackQuery, callback_data: dict):
    cur_state = dp.current_state()

    async with cur_state.proxy() as data:
        if not data.keys(): return

        if callback_data['choice'] == 'Писатели':
            await author_command(data['info'])
        elif callback_data['choice'] == 'Книжные серии':
            await series_command(data['info'])
        elif callback_data['choice'] == 'Книги':
            await find_books(data['info'])

    await call.answer()


async def spam_checking(message: types.Message):
    if len(message.text) >= 120 and message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP):
        await message.reply('Ваше сообщение похоже на спам или рекламу.\n'
                            'Администратор группы уведомлен')
        chat_admins = await bot.get_chat_administrators(message.chat.id)
        for admin in chat_admins:
            admin_id = admin.user.id
            text = f"Подозрительное сообщение от {message.from_user.get_mention()}\n{hlink('сообщение', message.url)}"
            if not admin.user.is_bot:
                await dp.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    reply_markup=report_reactions_keyboard(
                        message.from_user.id,
                        message.chat.id,
                        message.message_id)
                )
                await asyncio.sleep(0.05)
                return True

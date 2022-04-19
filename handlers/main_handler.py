from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.find_authors import author_command
from handlers.find_books import find_books
from handlers.find_series import series_command
from keyboards.inline.formats import get_requests, result_request
from loader import dp
from utils.throttlig import rate_limit
from utils.utils import create_list_choices


@rate_limit(limit=3)
@dp.message_handler()
async def main_handler(message: types.Message, state: FSMContext):
    '''
    Принимает запрос от юзера и выводит клавиатуру, с доступными вариантами (книги автора, книги, серии)
    '''
    if message.reply_to_message:
        return

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


@dp.callback_query_handler(result_request.filter())
async def current_result(call: types.CallbackQuery, callback_data: dict):
    cur_state = dp.current_state()

    async with cur_state.proxy() as data:
        if callback_data['choice'] == 'Писатели':
            await author_command(data['info'])
        elif callback_data['choice'] == 'Книжные серии':
            await series_command(data['info'])
        elif callback_data['choice'] == 'Книги':
            await find_books(data['info'])

    await call.answer()

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.channel_keyboards import edit_keyboard, post_keyboard, user_menu
from loader import dp


@dp.callback_query_handler(text='return', state='*')
async def return_to_edit_menu(call: types.CallbackQuery):
    # Нажание на кнопку "НАЗАД" во время режима редактирования
    await call.message.delete()


@dp.callback_query_handler(edit_keyboard.filter(action='quit'), state='*')
async def return_to_user_menu(call: types.CallbackQuery, callback_data: dict):
    # Нажатие на кнопку "НАЗАД" в режиме редактировать

    await call.message.edit_reply_markup(
        reply_markup=user_menu(post_id=callback_data['post_id'], user_id=call.message.from_user.id))


@dp.callback_query_handler(text='quit', state='*')
@dp.callback_query_handler(post_keyboard.filter(action='quit'), state='*')
async def current_result(call: types.CallbackQuery, state: FSMContext):
    # Нажание на кнопку "ОТМЕНИТЬ ПУБЛИКАЦИЮ"

    await call.message.edit_reply_markup()
    await state.finish()
    text = 'Ты вышел из режима публикаций\nЧтобы попробовать сначала жми /create_post'
    await call.message.edit_text(text)

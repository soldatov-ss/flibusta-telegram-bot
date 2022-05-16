from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.channels.strings import text_channel
from keyboards.inline.channel_keyboards import edit_keyboard, post_keyboard, edit_menu, user_menu, return_to_edit_key
from loader import dp, db
from states import UpgradePost
from utils.utils import check_link_for_channel


@dp.message_handler(state=UpgradePost.Post)
async def edit_post(message: types.Message, state: FSMContext):
    # Ловим измененное описание книги и обновляем в БД

    data = await state.get_data()
    if data:
        post_id = data['post_id']

        if data['action'] == 'book':
            post = await db.update_post(column='book', value=message.text, post_id=post_id)
        elif data['action'] == 'author':
            post = await db.update_post(column='author', value=message.text, post_id=post_id)
        elif data['action'] == 'description':
            post = await db.update_post(column='description', value=message.text, post_id=post_id)
        elif data['action'] == 'link':

            link = await check_link_for_channel(message.text, message)
            if not link:
                return await UpgradePost.Post.set()

            post = await db.update_post(column='link', value=message.text, post_id=post_id)

        text = text_channel(post)
        await message.answer(text, reply_markup=user_menu(post_id=post_id, user_id=message.from_user.id))

    await state.finish()



@dp.callback_query_handler(post_keyboard.filter(action='edit'), state='*')
async def post_menu(call: types.CallbackQuery, callback_data: dict):
    # Нажатие на кнопку "РЕДАКТИРОВАТЬ"
    post_id = callback_data['post_id']
    await call.message.edit_reply_markup(reply_markup=edit_menu(post_id=post_id))



@dp.callback_query_handler(edit_keyboard.filter(action='book'), state='*')
async def start_cmd_handler(call: types.CallbackQuery, state: FSMContext, callback_data: dict):

    await call.message.answer('Ок. Пришли новое название книги', reply_markup=return_to_edit_key)

    await UpgradePost.Post.set()
    async with state.proxy() as data:
        data['action'] = 'book'
        data['post_id'] = callback_data['post_id']
    await call.answer()


@dp.callback_query_handler(edit_keyboard.filter(action='author'), state='*')
async def start_cmd_handler(call: types.CallbackQuery, state: FSMContext, callback_data: dict):

    await call.message.answer('Ок. Пришли новое ФИО автора\n'
                              '<i>Если авторов несколько, пожалуйста, перечисли их ФИО через запятую</i>',
                              reply_markup=return_to_edit_key)

    await UpgradePost.Post.set()
    async with state.proxy() as data:
        data['action'] = 'author'
        data['post_id'] = callback_data['post_id']
    await call.answer()


@dp.callback_query_handler(edit_keyboard.filter(action='description'), state='*')
async def start_cmd_handler(call: types.CallbackQuery, state: FSMContext, callback_data: dict):

    await call.message.answer('Ок. Пришли новое описание книги', reply_markup=return_to_edit_key)

    await UpgradePost.Post.set()
    async with state.proxy() as data:
        data['action'] = 'description'
        data['post_id'] = callback_data['post_id']
    await call.answer()


@dp.callback_query_handler(edit_keyboard.filter(action='link'), state='*')
async def start_cmd_handler(call: types.CallbackQuery, state: FSMContext, callback_data: dict):

    await call.message.answer('Ок. Пришли новую ссылку на книгу', reply_markup=return_to_edit_key)

    await UpgradePost.Post.set()
    async with state.proxy() as data:
        data['action'] = 'link'
        data['post_id'] = callback_data['post_id']
    await call.answer()


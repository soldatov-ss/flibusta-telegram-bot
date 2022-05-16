from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from config import ADMIN_ID, channels
from handlers.channels.strings import text_channel
from keyboards.inline.admin import admin_menu, admin_keyboard
from keyboards.inline.channel_keyboards import post_keyboard, download_keyboard, go_to_channel
from loader import dp, db


@dp.callback_query_handler(post_keyboard.filter(action='send_to_admin'), state='*')
async def send_to_admin(call: types.CallbackQuery, callback_data: dict):
    # Отправляем админу сообщение о новом посте, запрашиваем одобрение на публикацию
    post_id = callback_data['post_id']
    post = await db.select_post(post_id)
    text = text_channel(post, from_admin=True)

    await dp.bot.send_message(ADMIN_ID, f'Новый пост для публикации\nCсылка: {post.get("link")}')
    await dp.bot.send_message(ADMIN_ID, text=text,
                              reply_markup=admin_menu(post_id, call.from_user.id))

    await call.message.edit_reply_markup()
    await call.message.answer('✅ Твой пост отправлен на модерацию!')



@dp.callback_query_handler(admin_keyboard.filter(action='post'))
async def post_channel(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # Создаем ссылку для кнопки в канале
    # Сообщаем юзеру что пост был одобрен

    post = await db.select_post(callback_data['post_id'])
    await call.message.edit_reply_markup()

    deep_link = await get_start_link(payload=post.get('link'), encode=True)
    channel_post = await call.message.send_copy(chat_id=channels,
                                 reply_markup=download_keyboard(post_id=callback_data['post_id'], link=deep_link))

    await dp.bot.send_message(
        chat_id=callback_data['user_id'], text=f'Твой пост был опубликован 🎉', reply_markup=go_to_channel(post_id=channel_post.message_id))



@dp.callback_query_handler(admin_keyboard.filter(action='reject'))
async def reject_post(call: types.CallbackQuery, callback_data: dict):

    await db.delete_post(post_id=callback_data['post_id'])
    await dp.bot.send_message(chat_id=callback_data['user_id'],
                              text='К сожалению, Ваша публикация была отклонена 🙄\nПопробуйте еще раз')



@dp.callback_query_handler(text='go_to_channel')
async def go_post(call: types.CallbackQuery):
    await call.answer()
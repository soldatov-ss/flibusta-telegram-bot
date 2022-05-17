from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_keyboard = CallbackData('channel_keyboard', 'action', 'post_id')
download_key = CallbackData('redirect_keyboard', 'post_id')
post_keyboard = CallbackData('edit_key', 'action', 'post_id', 'user_id')


def edit_menu(post_id: int):
    markup =  InlineKeyboardMarkup(row_width=1)
    for btn in [
            InlineKeyboardButton(text='Назад', callback_data=edit_keyboard.new(action='quit', post_id=post_id)),
            InlineKeyboardButton('Редактировать название книги', callback_data=edit_keyboard.new(action='book', post_id=post_id)),
            InlineKeyboardButton('Редактировать ФИО автора', callback_data=edit_keyboard.new(action='author', post_id=post_id)),
            InlineKeyboardButton('Редактировать описание', callback_data=edit_keyboard.new(action='description', post_id=post_id)),
            InlineKeyboardButton('Редактировать ссылку', callback_data=edit_keyboard.new(action='link', post_id=post_id))
    ]:
        markup.insert(btn)

    return markup



def user_menu(post_id: int, user_id: int):

    markup =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
            text='Отправить на модерацию', callback_data=post_keyboard.new(action='send_to_admin', post_id=post_id, user_id=user_id))
        ],
        [
            InlineKeyboardButton(
            text='Редактировать', callback_data=post_keyboard.new(action='edit', post_id=post_id, user_id=user_id)),
        InlineKeyboardButton(
            text='Отменить публикацию', callback_data=post_keyboard.new(action='quit', post_id=post_id, user_id=user_id))
        ]
    ], row_width=2)

    return markup



def go_to_channel(post_id: int):
    url = f'https://t.me/books_bar/{post_id}'

    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text='Перейти к публикации', callback_data='go_to_channel', url=url)
    markup.add(btn)

    return markup



def download_keyboard(post_id: int, link: str):

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text='Скачать книгу', callback_data=download_key.new(post_id), url=link))

    return markup




return_to_edit_btn = InlineKeyboardButton(text='Назад', callback_data='return')
return_to_edit_key = InlineKeyboardMarkup().add(return_to_edit_btn)


quit_btn = InlineKeyboardButton(text='Отменить публикацию', callback_data='quit')
quit_keyboard = InlineKeyboardMarkup().add(quit_btn)


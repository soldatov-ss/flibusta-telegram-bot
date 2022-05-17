from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

report_cb = CallbackData('report', 'user_id', 'chat_id', 'message_id', 'action')
admin_keyboard = CallbackData('admin_menu', 'action', 'post_id', 'user_id')


def report_reactions_keyboard(user_id, chat_id, message_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Забанить и удалить сообщение', callback_data=report_cb.new(
                    user_id=user_id, chat_id=chat_id, message_id=message_id, action='ban'
                )),
            ],
            [
                InlineKeyboardButton('Забанить и удалить всё', callback_data=report_cb.new(
                    user_id=user_id, chat_id=chat_id, message_id=message_id, action='ban_delete'
                ))
            ],
            [
                InlineKeyboardButton('Удалить сообщение', callback_data=report_cb.new(
                    user_id=user_id, chat_id=chat_id, message_id=message_id, action='delete'
                )),
            ]
        ]
    )





def admin_menu(post_id: int, user_id: int):
    markup =  InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text='Опубликовать', callback_data=admin_keyboard.new('post', post_id, user_id)),
        InlineKeyboardButton(text='Отклонить', callback_data=admin_keyboard.new('reject', post_id, user_id)),
        InlineKeyboardButton(text='Редактировать', callback_data=admin_keyboard.new('edit', post_id, user_id)),
        ]
    ], row_width=2)

    return markup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

report_cb = CallbackData('report', 'user_id', 'chat_id', 'message_id', 'action')


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

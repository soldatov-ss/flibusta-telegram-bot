from aiogram import Dispatcher
from .is_reply import IsReplyFilter
from .chat_filters import IsGroup, IsPrivate

def setup(dp: Dispatcher):
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]

    dp.filters_factory.bind(IsReplyFilter, event_handlers=text_messages)
    dp.filters_factory.bind(IsGroup, event_handlers=text_messages)
    dp.filters_factory.bind(IsPrivate, event_handlers=text_messages)

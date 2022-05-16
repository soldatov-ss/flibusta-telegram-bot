import hashlib

from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.utils.deep_linking import decode_payload

from loader import db
from utils.parsing.general import get
from .check_args import check_args


async def get_message_text(message: types.Message | FSMContextProxy, method: str):
    '''
    Принимает запрос с комманды либо с FSM и отдает готовый объект Message
    '''
    if message.is_command():
        current_res = message.get_args()
        empty_message = check_args(current_res, method)
        if empty_message:
            await message.answer(empty_message)
            return
    else:
        current_res = message.text

    return current_res


def check_link(link: str):
    # /b_101112@my_flibusta_bot
    link = link.replace('_', '/')
    if '@' in link:
        link = link[:link.find('@')]
    # /b/101112
    return link


def create_current_name(chat_type: str, name: str, flag=False):
    # Проверка, откуда запрос, с бота или с группы ибо есть ограничения в боте, в группе же нету
    # Хешируем, чтобы обойти ограничение в 64 байта для CallbackData

    if chat_type == 'private':
        current_item = 'bot' + name
    else:
        current_item = 'group' + name
    if not flag:  # Только для авторов и книг с серии
        current_item_hash = hashlib.md5(current_item.encode()).hexdigest()
    else:
        current_item_hash = current_item
    return current_item_hash



async def check_link_for_channel(link: str, message: types.Message):
    '''
    Проверка ссылки для публикации в канале
    '''
    url = f'http://flibusta.is{link}'
    link = message.text.replace("_", '/')

    if link.startswith('/a') or link.startswith('/series'):
        await message.answer('‼ Ссылка должна быть на конкретную КНИГУ\n '
                             '(не на автора и не на книжную серию)')
        return

    data = await db.select_book(link=link)

    if data and data.get('description'):
        return True
    else:
        try:
            await get(url)
        except:
            await message.answer('‼ Такой ссылки у меня в базе нет\n'
                                 'Убедись что ссылка в формате /b_00000')
            return

    return True


def check_link_from(message: types.Message):
    '''
    Проверяем, поступила ли ссылка с канала или с хендлера
    :return: /b/12344
    '''
    if message.text.startswith('/start'):
        book_link = decode_payload(''.join(message.text.split()[1:]))
        link = check_link(book_link)  # обрезаем лишнее в ссылке
    else:
        link = check_link(message.text)
    return link



def replace_symbols(value):
    '''
    Убираем лишнее, чтобы добавить в БД
    :param value: <tex't>
    :return: text
    '''
    return value.replace("'", '"').replace(">", ')').replace('<', '(')

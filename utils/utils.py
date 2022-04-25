import hashlib

from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy

from .check_args import check_args
from utils.parsing.general import get_without_register, get
from .pages.strings import no_result_message


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


async def create_list_choices(message: types.Message):
    '''
    Возвращает список вариантов для инлайн клавиатуры в main_handler
    '''
    url = f'http://flibusta.is//booksearch?ask={message.text}&chs=on&cha=on&chb=on'
    if message.chat.id == 415348636:
        soup = await get_without_register(url)
    else:
        soup = await get(url)

    result = []
    for i in soup.find_all('h3'):
        if not i.text.split()[1] in ('серии', 'писатели', 'книги'):
            continue
        if i.text.split()[1] == 'серии':
            result.append('Книжные серии')
        else:
            result.append(i.text.split()[1].title())
    if not result:
        empty_message = no_result_message(method='book')
        await message.answer(empty_message)
        return

    return result


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

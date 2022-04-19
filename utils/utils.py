from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy

from utils.check_args import check_args
from utils.pages.strings import strings_for_user_into_bot
from utils.parsing.general import get_without_register, get


async def get_message_text(message: types.Message | FSMContextProxy, method: str):
    '''
    Принимает запрос с комманды либо с FSM и отдает готовый объект Message
    '''
    if message.is_command():
        current_res = message.get_args()
        empty_message = check_args(current_res, method)
        if empty_message:
            return await message.answer(empty_message)

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
        empty_message = strings_for_user_into_bot(no_result_message='book')
        await message.answer(empty_message)
        return

    return result
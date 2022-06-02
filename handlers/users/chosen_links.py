import re

from aiogram import types

from handlers.users.find_authors import current_languages
from keyboards.inline.other_keyboards import get_language, get_formats
from loader import bot
from loader import dp, db
from utils.parsing.authors import languages
from utils.parsing.other import get_book_description
from utils.throttlig import rate_limit
from utils.utils import check_link, check_link_from


@rate_limit(limit=3)
@dp.message_handler(regexp=re.compile(r'(^/a_\d+)|(^/a_\d+@)'))
async def chosen_link_author(message: types.Message):
    # Ловим линк и выводим доступные варинаты языков на которых написаны книги
    link = check_link(message.text)
    url = f'http://flibusta.is{link}&lang='

    data = await db.get_author_language(link, message.chat.type)

    if data:
        languages_lst, lang_abbr, author = data
        lang_abbr = lang_abbr.split(':')
        languages_lst = languages_lst.split(':')
        await db.update_count(table='authors', column='queries', link=link)

    else:
        soup = await bot.get('session').get_soup(url, chat=message.chat)
        lang_abbr, languages_lst, author = languages(soup)
        await db.create_or_update_author(author, link, message.chat.type, ':'.join(lang_abbr), ':'.join(languages_lst))

    if len(lang_abbr) == 1:
        await current_languages(message, {"abbr": lang_abbr[0], 'link': link})
    else:

        text = f'Книги доступны на следующих языках: \n' \
               f'Ты можешь выбрать удобный для тебя язык 👇'

        await message.answer(text, reply_markup=get_language(
            languages_lst=languages_lst, link=link, abbr_lst=lang_abbr))



@rate_limit(limit=2)
@dp.message_handler(regexp=re.compile(r'(^/b_\d+)|(^/b_\d+@.+)'))
async def chosen_link_book(message: types.Message):
    # Ловим линк и выводим доступные форматы для скачивания

    link = check_link_from(message)
    book, author, file_formats, descr = await get_book_description(link)

    text = f'Автор: <b>{author}</b>\n\n' \
           f'📖 <b>{book}</b>\n\n' \
           f'Описание: \n' \
           f'<i>{descr}</i>'

    await message.answer(text=text, reply_markup=get_formats(formats_lst=file_formats, link=link))

from aiogram import md


def text_channel(data: dict, from_admin: bool = False):
    author = list(map(lambda x: x.replace(" ", ""), data.get("author").split(',')))
    author = ',  #'.join(author)

    url = md.hide_link(data.get("url"))
    text = f'📕 <b>{data.get("book")}</b>\n' \
           f'#{author}\n\n' \
           f'<i>{data.get("description")}</i>\n' \
           f'{url}'

    if not from_admin:
        text += f'RU Ссылка {data.get("ru_link")}\nUA Ссылка {data.get("ua_link")}'
    return text
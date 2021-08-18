def page_rating(rating_dict: dict, descr):
    # обработка страницы с рейтингом
    rating_lst = []
    i = 0
    if not rating_dict:
        return f'На данный момент рейтинг пуст'
    for link, book in rating_dict.items():
        if i == 0:
            text = f'🏆  <b>{descr}</b>  🏆\n\n\n' \
                   f'🥇 <b>{book}</b>\n' \
                   f'Описание: /{link}\n\n'
            rating_lst.append(text)
        elif i == 1:
            text = f'🥈 <b>{book}</b>\n' \
                   f'Описание: /{link}\n\n'
            rating_lst.append(text)
        elif i == 2:
            text = f'🥉 <b>{book}</b>\n' \
                   f'Описание: /{link}\n\n'
            rating_lst.append(text)
        elif i > 2:
            text = f'📕<b>{book}</b>\n' \
                   f'Описание: /{link}\n\n'
            rating_lst.append(text)
        i += 1
    return ' '.join(rating_lst)

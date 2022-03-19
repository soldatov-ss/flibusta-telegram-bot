def check_args(item: str, value: str):
    text = ''
    if value == 'author':
        author = item
        if not author:
            text = 'Нужно также указать ФИО автора ☺\n\n' \
                   'Попробуй так:\n' \
                   '/author <i>ФИО автора</i>\n\n ' \
                   'Например:\n' \
                   '/author Стивен Кинг\n' \
                   '/author Толкин'
        elif len(author) <= 2:
            text = '❗Слишком короткий запрос. Попробуй еще раз❗'

    elif value == 'book':
        if len(item) <= 2:
            text = '❗Слишком короткое название, попробуй еще раз❗'

    elif value == 'series':
        series = item
        if not series:
            text = 'Нужно также указать название книжной серии ☺\n' \
                   'Попробуй так:\n' \
                   '/series <i>название книжной серии</i>\n\n' \
                   'Например:\n' \
                   '/series Гарри Поттер\n' \
                   '/series Ведьмак'
        elif len(series) <= 2:
            text = '❗Слишком короткое название, попробуй еще раз❗'

    return text

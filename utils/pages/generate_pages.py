from utils.pages.strings import book_strings, author_strings, author_books_strings, series_strings, series_book_strings


def create_pages(books_dict: dict, count_items, flag) -> list:
    # Разбиение всех найденных книг по 5 книг на страницу и добавление всего в массив массивов
    # book_lst = [[book_1, book_2, book_3, book_4, book_5], [book_1, book_2, book_3, book_4, book_5]]

    page_with_5_books = []
    i = 1
    my_str, first_text, other_text = '', '', ''

    for key, item in books_dict.items():
        if flag == 'books':
            first_text, other_text = book_strings(count_items, book=item[0],
                                                  author=item[1], link=key)
        elif flag == 'authors':
            first_text, other_text = author_strings(count_items, author=item, link=key)

        elif flag == 'author_books':
            first_text = author_books_strings(book=item, link=key)
            other_text = first_text
        elif flag == 'series':
            first_text, other_text = series_strings(count_series=count_items, series=item, link=key)
        elif flag == 'series_books':
            first_text, other_text = series_book_strings(count_book=count_items, book=item, link=key)

        if count_items < 5:
            # Если кол-во книг меньше 5
            if i == 1:
                my_str += first_text
            else:
                my_str += other_text
            i += 1

        if count_items >= 5:
            if i == 1:
                my_str += first_text
            elif i % 5 != 0:
                my_str += other_text
            elif i % 5 == 0:
                my_str += other_text
                page_with_5_books.append([my_str])
                my_str = ''
            i += 1
    page_with_5_books.append([my_str]) if my_str else None
    return page_with_5_books


def get_page(items_list, page: int = 1, author=None, series_lst=None):
    # Получаем страницу из списка книг/авторов
    page_index = page - 1

    if author:  # Добавляем шапку на страницу с книгами авторов
        author, count_books = author
        text = f'<b>{author}</b>\n\n' \
               f'📚Книг найдено: <b>{count_books}</b>  🔍\n\n'
        if text not in items_list[page_index][0]:
            items_list[page_index] = [text + '' + items_list[page_index][0]]

    if series_lst:  # Шапка на страницу с описанием серии
        name, series_authors, genres = series_lst
        text = f'📚<b>{name}</b>\n' \
               f'<pre>{series_authors}</pre>\n' \
               f'<pre>{genres}</pre>\n\n'
        if text not in items_list[page_index][0]:
            items_list[page_index] = [text + '' + items_list[page_index][0]]

    return ' '.join(items_list[page_index])

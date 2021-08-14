from utils.strings import book_strings, author_strings, author_books


def create_pages(books_dict: dict, max_books, flag, author=None) -> list:
    # Разбиение всех найденных книг по спискам для вывода
    page_with_5_books = []
    i = 1
    my_str, first_text, other_text = '', '', ''

    for key, item in books_dict.items():
        if flag == 'books':
            first_text, other_text = book_strings(max_books, book=item[0],
                                                  author=item[1], link=key)
        elif flag == 'authors':
            first_text, other_text = author_strings(max_books, author=item, link=key)

        elif flag == 'author_books':
            first_text = author_books(book=item, link=key)
            other_text = first_text
        if max_books < 5:
            # Если кол-во книг меньше 5
            if i == 1:
                my_str += first_text
            else:
                my_str += other_text
            i += 1

        if max_books >= 5:
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


def get_page(items_list, page: int = 1, author=None):
    # Получаем страницу из списка книг/авторов
    page_index = page - 1
    if author:  # Добавляем шапку на страницу с книгами авторов
        text = f'<b>{author}</b>\n\n\n'
        if text not in items_list[page_index][0]:
            items_list[page_index] = [text + '' + items_list[page_index][0]]

    return ' '.join(items_list[page_index])

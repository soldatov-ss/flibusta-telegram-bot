from pprint import pprint

def page_strings(max_books, author, book, link):
    link = link[1:].replace('/', '_', 1)
    first_text = f'🔎  Найдено всего книг: {max_books}  🔍\n\n' \
                 f'📖 <b>{book}</b> -- <i>{author}</i> \n\n' \
                 f'⬇ Скачать: /{link}\n\n\n'

    other_text = f'📖 <b>{book}</b> -- <i>{author}</i> \n\n' \
                 f'⬇ Скачать: /{link}\n\n\n' \


    return first_text, other_text


def create_pages(books_dict: dict, max_books) -> list:
    # Разбиение всех найденных книг по спискам для вывода
    page_with_5_books = []
    i = 1
    my_str = ''

    for key, item in books_dict.items():
        first_text, other_text = page_strings(max_books, book=item[0],
                                              author=item[1], link=key)

        if max_books < 5:
            # Если кол-во книг меньше 5
            if i == 1:
                my_str += first_text
            else:
                my_str += other_text
            i += 1

        if max_books > 5:
            if i == 1:
                my_str += first_text
            elif i % 5 != 0:
                my_str += other_text
            elif i % 5 == 0:
                my_str += other_text
                page_with_5_books.append([my_str])
                my_str = ''
            i += 1
    page_with_5_books.append([my_str])
    return page_with_5_books


def get_page(book_list, page: int = 1):
    page_index = page - 1
    return book_list[page_index]

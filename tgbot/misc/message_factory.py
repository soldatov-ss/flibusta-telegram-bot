def get_author_missing_args_message() -> str:
    return (
        "Please specify the author's name to search.\n"
        "For example: /author <i>first name</i> <i>last name</i>\n"
        "Example: /author Stephen King"
    )


def get_missing_book_sequence_args_message() -> str:
    return (
        "Please specify the book sequence name to search.\n"
        "For example: /sequence <i>sequence name</i>\n"
        "Example: /sequence Game of Thrones"
    )

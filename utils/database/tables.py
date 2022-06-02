def create_tables_rows():
    #  Таблица для хранения пользователей
    users = '''
    CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    telegram_id BIGINT NOT NULL UNIQUE,
    amount BIGINT DEFAULT 0
    )
    '''
    # таблица для храниния книг
    books = '''
    CREATE TABLE IF NOT EXISTS books (
    book_id SERIAL PRIMARY KEY,
    book_name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL UNIQUE,
    downloaded BIGINT NOT NULL,
    author VARCHAR(255),
    formats VARCHAR(255),
    description TEXT
    )
    '''
    authors = '''
    CREATE TABLE IF NOT EXISTS authors (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL UNIQUE,
    queries BIGINT NOT NULL,
    private_langs_abbr VARCHAR(255),
    group_langs_abbr VARCHAR(255),
    group_langs VARCHAR(255),
    private_langs VARCHAR(255)
    )
    '''
    # Таблица для хранения страниц с результатами запросов и названиями запросов
    book_pages = '''
    CREATE TABLE IF NOT EXISTS book_pages (
    pages_id SERIAL PRIMARY KEY,
    request_name VARCHAR(255) NOT NULL UNIQUE,
    pages text[]
    )
    '''
    # Хранение страниц с авторами
    author_pages = '''
    CREATE TABLE IF NOT EXISTS author_pages (
    pages_id SERIAL PRIMARY KEY,
    request_name VARCHAR(255) NOT NULL UNIQUE,
    pages text[]
    )
    '''
    # Страницы с книжными сериями по запросу
    series_pages = '''
    CREATE TABLE IF NOT EXISTS series_pages (
    pages_id SERIAL PRIMARY KEY,
    request_name VARCHAR(255) NOT NULL UNIQUE,
    pages text[]
    )
    '''
    # Книги по выбронному автору
    author_books_pages = '''
    CREATE TABLE IF NOT EXISTS author_book_pages (
    pages_id SERIAL PRIMARY KEY,
    request_name VARCHAR(255) NOT NULL UNIQUE,
    author_name VARCHAR(255),
    сount_books INT, 
    pages text[]
    )
    '''
    # Книги по выбранной серии
    series_books_pages = '''
    CREATE TABLE IF NOT EXISTS series_book_pages (
    pages_id SERIAL PRIMARY KEY,
    request_name VARCHAR(255) NOT NULL UNIQUE,
    series_name VARCHAR(255),
    series_author VARCHAR(255), 
    series_genres VARCHAR(255),
    pages text[]
    )
    '''

    book_formats = '''
    CREATE TABLE IF NOT EXISTS book_formats (
    format_id  SERIAL PRIMARY KEY,
    book_id  INT NOT NULL UNIQUE,
    fb2 VARCHAR(255), 
    epub VARCHAR(255), 
    mobi VARCHAR(255), 
    download VARCHAR(255),
    FOREIGN KEY(book_id) REFERENCES books(book_id)
    )
    '''

    channel_post = '''
    CREATE TABLE IF NOT EXISTS channel_post (
    post_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, 
    url VARCHAR(255) UNIQUE NOT NULL,
    book  VARCHAR(255),
    author VARCHAR(255),
    link VARCHAR(255),
    description TEXT
    )
    '''

    return [users, books, authors, book_pages, author_pages, series_pages,
                       author_books_pages, series_books_pages, book_formats, channel_post]
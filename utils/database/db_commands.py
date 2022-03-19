from typing import Union

import asyncpg
from asyncpg import Connection, UniqueViolationError
from asyncpg.pool import Pool

import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)  # - все записи списком
                elif fetchval:
                    result = await connection.fetchval(command, *args)  # - одна запись
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)  # - первая строка
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_tables(self):

        #  Таблица для хранения пользователей
        create_table_user = '''
        CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        )
        '''
        # таблица для храниния рейтинга скачанных книг
        create_table_books = '''
        CREATE TABLE IF NOT EXISTS books (
        book_id SERIAL PRIMARY KEY,
        book_name VARCHAR(255) NOT NULL,
        link VARCHAR(255) NOT NULL UNIQUE,
        downloaded BIGINT NOT NULL
        )
        '''
        create_table_authors = '''
        CREATE TABLE IF NOT EXISTS authors (
        author_id SERIAL PRIMARY KEY,
        author_name VARCHAR(255) NOT NULL,
        link VARCHAR(255) NOT NULL UNIQUE,
        queries BIGINT NOT NULL
        )
        '''
        # Таблица для хранения страниц с результатами запросов и названиями запросов
        create_table_book_pages = '''
        CREATE TABLE IF NOT EXISTS book_pages (
        pages_id SERIAL PRIMARY KEY,
        request_name VARCHAR(255) NOT NULL UNIQUE,
        pages text[]
        )
        '''
        # Хранение страниц с авторами
        create_table_author_pages = '''
        CREATE TABLE IF NOT EXISTS author_pages (
        pages_id SERIAL PRIMARY KEY,
        request_name VARCHAR(255) NOT NULL UNIQUE,
        pages text[]
        )
        '''
        # Страницы с книжными сериями по запросу
        create_table_series_pages = '''
        CREATE TABLE IF NOT EXISTS series_pages (
        pages_id SERIAL PRIMARY KEY,
        request_name VARCHAR(255) NOT NULL UNIQUE,
        pages text[]
        )
        '''
        # Книги по выбронному автору
        create_table_author_books_pages = '''
        CREATE TABLE IF NOT EXISTS author_book_pages (
        pages_id SERIAL PRIMARY KEY,
        request_name VARCHAR(255) NOT NULL UNIQUE,
        author_name VARCHAR(255),
        сount_books INT, 
        book_pages text[]
        )
        '''
        # Книги по выбранной серии
        create_table_series_books_pages = '''
        CREATE TABLE IF NOT EXISTS series_book_pages (
        pages_id SERIAL PRIMARY KEY,
        request_name VARCHAR(255) NOT NULL UNIQUE,
        series_name VARCHAR(255),
        series_author VARCHAR(255), 
        series_genres VARCHAR(255),
        book_pages text[]
        )
        '''
        await self.execute(create_table_user, execute=True)
        await self.execute(create_table_books, execute=True)
        await self.execute(create_table_authors, execute=True)
        await self.execute(create_table_book_pages, execute=True)
        await self.execute(create_table_author_pages, execute=True)
        await self.execute(create_table_series_pages, execute=True)
        await self.execute(create_table_author_books_pages, execute=True)
        await self.execute(create_table_series_books_pages, execute=True)

    async def add_user(self, user: str, telegram_id: int):
        # Добавляет каждого нового пользователя в базу
        sql = f"INSERT INTO users(full_name, telegram_id) VALUES ('{user}', {telegram_id})"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def rating_book(self, book: str, link: str):
        # Добавляет книгу в рейтинг, если уже есть в таблице - обновляет счетчик скачанных книг
        sql = f"INSERT INTO books(book_name, link, downloaded) VALUES ('{book}', '{link}', {1})"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            count = await self.execute(f"SElECT downloaded FROM books WHERE link = '{link}'", fetchval=True)
            sql = f"UPDATE books SET downloaded = {count + 1} WHERE link = '{link}'"
            await self.execute(sql, execute=True)

    async def rating_author(self, author: str, link: str):
        # Добавляет автора в рейтинг, если уже есть в табл - обновляет счетчик скачанных книг
        sql = f"INSERT INTO authors(author_name, link, queries) VALUES ('{author}', '{link}', {1})"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            count = await self.execute(f"SElECT queries FROM authors WHERE link = '{link}'", fetchval=True)
            sql = f"UPDATE authors SET queries = {count + 1} WHERE link = '{link}'"
            await self.execute(sql, execute=True)

    async def select_all_users(self):
        count = await self.execute('SELECT count(*) FROM users', fetchval=True)
        return count

    async def select_all_books(self):
        count = await self.execute('SELECT count(*) FROM books', fetchval=True)
        return count

    async def select_top_books(self):
        # Возвращаем топ 10 книг по скачиванию
        top = await self.execute('SELECT * FROM books ORDER BY downloaded DESC LIMIT 10', fetch=True)
        top_dict = {}
        for elem in top:
            link = elem.get('link')
            link = link[1:].replace('/', '_', 1)
            top_dict[link] = elem.get('book_name')

        return top_dict

    async def select_top_authors(self):
        # Возвращаем топ 10 авторов по запросам
        top = await self.execute('SELECT * FROM authors ORDER BY queries DESC LIMIT 10', fetch=True)
        top_dict = {}
        for elem in top:
            link = elem.get('link')
            link = link[1:].replace('/', '_', 1)
            top_dict[link] = elem.get('author_name')

        return top_dict

    #
    # Функции для массивов
    #
    async def add_new_pages(self, table_name, items, request_name):
        sql = f"INSERT INTO {table_name}(request_name, pages) VALUES ('{request_name}', ARRAY[{items}])"

        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def add_new_author_book_pages(self, items, request_name, count_books=None, author=None):
        sql = f"""INSERT INTO author_book_pages(request_name, author_name, сount_books, book_pages)
                    VALUES ('{request_name}', '{author}', {count_books}, ARRAY[{items}])"""
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def add_new_series_book_pages(self, items, request_name, series_name, series_author, series_genres):
        sql = f"""INSERT INTO series_book_pages(request_name, series_name, series_author, series_genres, book_pages)
                    VALUES ('{request_name}', '{series_name}', '{series_author}', '{series_genres}', ARRAY[{items}])"""
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def find_pages(self, request_name, table_name):
        sql = f"SELECT request_name, pages FROM {table_name} WHERE request_name = '{request_name}'"
        res = await self.execute(sql, fetch=True)
        if not res: return

        name = res[0].get('request_name')
        book_pages = res[0].get('pages')
        book_pages = [list(map(lambda x: x.replace('\\n', '\n'), elem)) for elem in
                      book_pages[0]]  # убираем экранирование с postgresql

        return name, book_pages

    async def author_pages(self, request_name):
        sql = f"SELECT request_name, author_name, book_pages, сount_books FROM author_book_pages WHERE request_name = '{request_name}'"
        res = await self.execute(sql, fetch=True)
        if not res: return

        name = res[0].get('request_name')
        pages_lst = res[0].get('book_pages')
        pages_lst = [list(map(lambda x: x.replace('\\n', '\n'), elem)) for elem in
                     pages_lst[0]]  # убираем экранирование с postgresql
        author_name = res[0].get('author_name')
        count_books = res[0].get('сount_books')

        return name, pages_lst, author_name, count_books

    async def series_pages(self, request_name):
        sql = f"SELECT request_name, series_name, series_author, series_genres, book_pages FROM series_book_pages WHERE request_name = '{request_name}'"
        res = await self.execute(sql, fetch=True)
        if not res: return

        name = res[0].get('request_name')
        series_pages = res[0].get('book_pages')
        series_pages = [list(map(lambda x: x.replace('\\n', '\n'), elem)) for elem in
                        series_pages[0]]  # убираем экранирование с postgresql
        series_info = [res[0].get('series_name'), res[0].get('series_author'), res[0].get('series_genres')]

        return name, series_pages, series_info

    async def delete_table_pages(self):
        await self.execute(f'DROP TABLE book_pages, author_book_pages, series_pages', execute=True)

    async def update_book_pages(self, request_name, pages, table_name, column='pages'):
        sql = f"UPDATE {table_name} SET {column} = ARRAY[{pages}] WHERE request_name='{request_name}'"
        await self.execute(sql, execute=True)

    async def update_author_pages(self, pages: list, request_name: str, count_books: int):
        sql = f"""
                UPDATE author_book_pages SET book_pages = ARRAY[{pages}],
                сount_books = {count_books} WHERE request_name = '{request_name}'
                """
        await self.execute(sql, execute=True)

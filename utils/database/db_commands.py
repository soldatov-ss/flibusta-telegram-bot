from typing import Union

import asyncpg
from asyncpg import Connection
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
        queries BIGINT NOT NULL
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
        list_tables = [users, books, authors, book_pages, author_pages, series_pages,
                       author_books_pages, series_books_pages, book_formats]

        for table in list_tables:
            await self.execute(table, execute=True)

    async def add_user(self, user: str, telegram_id: int):
        # Добавляет каждого нового пользователя в базу
        sql = f"INSERT INTO users(full_name, telegram_id, amount) VALUES ('{user}', {telegram_id}, 0) ON CONFLICT  DO NOTHING"
        await self.execute(sql, execute=True)


    async def update_user_downloads(self, user_id: int):
        # Обновляет кол-во загрузок у юзера
        sql = f'''
                UPDATE users
                SET amount = amount + 1
                WHERE telegram_id = {user_id}
                '''
        await self.execute(sql, execute=True)


    async def insert_book(self, book: str, link: str, author: str, formats: str, description: str):
        sql = f'''
            INSERT INTO books(book_name, link, downloaded, author, formats, description)  
            VALUES('{book}', '{link}', 1, '{author}', '{formats}', '{description}')
            ON CONFLICT (link) DO UPDATE SET 
            author = '{author}',
            formats = '{formats}',
            description = '{description}' 
            '''
        await self.execute(sql, execute=True)


    async def select_file_id(self, link, format):
        # Получаем file_id книги
        sql = f'''
            SELECT {format} FROM book_formats 
            JOIN books USING(book_id) 
            WHERE link = '{link}'
        '''
        return await self.execute(sql, fetchval=True)

    async def insert_file_id(self, link, format, file_id):
        # Обновляем file_id к соответствующему формату
        sql = f'''
            INSERT INTO book_formats (book_id, {format}) VALUES 
            ((SELECT book_id FROM books WHERE link = '{link}'), '{file_id}') 
            ON CONFLICT (book_id) DO UPDATE
            SET {format} = '{file_id}'
        '''
        return await self.execute(sql, fetchval=True)


    async def update_count_downloaded(self, link: str):
        # Обновляем рейтинг выбранной книги
        sql = f'''
            UPDATE books SET
             downloaded = 1 + downloaded
            WHERE link = '{link}'
        '''
        await self.execute(sql, execute=True)


    async def select_book(self, link):
        sql = f'''
            SELECT book_name, author, formats, description FROM BOOKS WHERE link = '{link}'
                '''
        res = await self.execute(sql, fetchrow=True)
        return res if res else None


    async def rating_author(self, author: str, link: str):
        # Добавляет автора в рейтинг, если уже есть в табл - обновляет счетчик скачанных книг
        sql = f'''INSERT INTO authors(author_name, link, queries) VALUES ('{author}', '{link}', 1)
                    ON CONFLICT (link) DO UPDATE 
                    SET queries = 1 + (SELECT queries from authors where link = '{link}')'''
        await self.execute(sql, execute=True)

    async def select_count_values(self, table_name):
        # Выводит кол-во скачанных книг, либо кол-во юзеров
        count = await self.execute(f'SELECT count(*) FROM {table_name}', fetchval=True)
        return count

    async def rating_top_10_values(self, table):
        # Возвращаем топ 10 книг или авторов по запросам и скачиваниям
        query = 'downloaded' if table == 'book' else 'queries'
        top = await self.execute(f'SELECT * FROM {table}s ORDER BY {query} DESC LIMIT 10', fetch=True)
        top_dict = {}
        for elem in top:
            link = elem.get('link')
            link = link[1:].replace('/', '_', 1)
            top_dict[link] = elem.get(f'{table}_name')

        return top_dict

    async def delete_table_pages(self):
        await self.execute(f'DROP TABLE book_pages, author_book_pages, series_pages', execute=True)

    #
    # Функции для массивов
    #
    async def add_new_pages(self, table_name, items, request_name):
        sql = f"""
        INSERT INTO {table_name}(request_name, pages) 
        VALUES ('{request_name}', ARRAY[{items}]) ON CONFLICT  DO NOTHING
        """

        await self.execute(sql, execute=True)

    async def add_new_author_book_pages(self, items, request_name, count_books, author):
        sql = f"""INSERT INTO author_book_pages(request_name, author_name, сount_books, pages)
                    VALUES ('{request_name}', '{author}', {count_books}, ARRAY[{items}])
                    ON CONFLICT DO NOTHING"""
        await self.execute(sql, execute=True)

    async def add_new_series_book_pages(self, items, request_name, series_name, series_author, series_genres):
        sql = f"""INSERT INTO series_book_pages(request_name, series_name, series_author, series_genres, pages)
                    VALUES ('{request_name}', '{series_name}', '{series_author[:250]}', '{series_genres}', ARRAY[{items}])
                    ON CONFLICT  DO NOTHING"""
        await self.execute(sql, execute=True)

    async def select_pages(self, request_name, table_name, *args):
        if args:
            sql = f"SELECT request_name, {', '.join(args)} FROM {table_name} WHERE request_name = '{request_name}'"
        else:
            sql = f"SELECT request_name, pages FROM {table_name} WHERE request_name = '{request_name}'"

        res = await self.execute(sql, fetch=True)
        if not res: return

        return self.get_args(res[0], table_name)

    async def update_author_pages(self, pages: list, request_name: str, count_books: int):
        sql = f"""
                UPDATE author_book_pages SET pages = ARRAY[{pages}],
                сount_books = {count_books} WHERE request_name = '{request_name}'
                """
        await self.execute(sql, execute=True)

    async def update_book_pages(self, request_name, pages, table_name, column='pages'):
        sql = f"UPDATE {table_name} SET {column} = ARRAY[{pages}] WHERE request_name='{request_name}'"
        await self.execute(sql, execute=True)

    @staticmethod
    def get_args(result, table_name):
        name = result.get('request_name')
        pages_lst = [list(map(lambda x: x.replace('\\n', '\n'), elem)) for elem in result.get('pages')[0]]

        if table_name == 'author_book_pages':
            author_name = result.get('author_name')
            count_books = result.get('сount_books')
            return name, pages_lst, author_name, count_books
        elif table_name == 'series_book_pages':

            series_info = [result.get('series_name'), result.get('series_author'), result.get('series_genres')]
            return name, pages_lst, series_info
        else:
            return name, pages_lst

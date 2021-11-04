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

    async def create_table_users(self):

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
        create_table_pages = '''
        CREATE TABLE IF NOT EXISTS pages (
        pages_id SERIAL PRIMARY KEY,
        request_name VARCHAR(255) UNIQUE,
        book_pages text[]
        )
        '''
        await self.execute(create_table_user, execute=True)
        await self.execute(create_table_books, execute=True)
        await self.execute(create_table_authors, execute=True)
        await self.execute(create_table_pages, execute=True)

    async def add_user(self, user: str, telegram_id: int):
        # Добавляет каждого нового пользователя в базу
        sql = f"INSERT INTO users(full_name, telegram_id) VALUES ('{user}', {telegram_id})"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def add_book(self, book: str, link: str):
        # Добавляет книгу в рейтинг, если уже есть в таблице - обновляет счетчик скачанных книг
        sql = f"INSERT INTO books(book_name, link, downloaded) VALUES ('{book}', '{link}', {1})"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            count = await self.execute(f"SElECT downloaded FROM books WHERE link = '{link}'", fetchval=True)
            sql = f"UPDATE books SET downloaded = {count + 1} WHERE link = '{link}'"
            await self.execute(sql, execute=True)

    async def add_author(self, author: str, link: str):
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
    async def add_new_pages(self, items, request_name):

        sql = f"INSERT INTO pages(request_name, book_pages) VALUES ('{request_name}', ARRAY[{items}])"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def find_pages(self, request_name):
        sql = f"SELECT request_name, book_pages FROM pages WHERE request_name = '{request_name}'"
        try:
            res = await self.execute(sql, fetch=True)
            name = res[0].get('request_name')
            res_lst = res[0].get('book_pages')
            res_lst = [list(map(lambda x: x.replace('\\n', '\n'), elem)) for elem in
                       res_lst[0]]  # убираем экранирование с postgresql

        except IndexError:
            return
        else:
            return name, res_lst



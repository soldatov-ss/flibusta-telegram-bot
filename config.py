from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')

# настройки входа на сайт
CITE_PASS = env.str('CITE_PASS')
CITE_LOGIN = env.str('CITE_LOGIN')


# настройки входа в БД
DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')

CHAT_ID = env.str('ADMINS')
GROUP_ID = env.str('GROUP_ID')
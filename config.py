from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')

# настройки входа на сайт
SITE_PASS = env.str('SITE_PASS')
SITE_LOGIN = env.str('SITE_LOGIN')


# настройки входа в БД
DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')

ADMIN_ID = env.str('ADMINS')
GROUP_ID = env.str('GROUP_ID')
channels = env.str('CHANNEL_ID')

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime}: {levelname}: {name}: {module}-{funcName}={lineno}: {message}',
            'style': '{'
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'level': 'ERROR',
            'formatter': 'std_format'
        }
    },

    'loggers': {
        'app_logger': {
            'level': 'ERROR',
            'handlers': ['console']
        }
    }
}
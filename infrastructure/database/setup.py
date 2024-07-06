from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from tgbot.config import Config, DbConfig, load_config

config: Config = load_config(".env")


def create_engine(db: DbConfig, echo=False):
    engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
    )
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool


engine = create_engine(config.db, echo=True)
session_pool = create_session_pool(engine)

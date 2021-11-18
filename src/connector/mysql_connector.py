# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:14
import contextlib
from asyncio import current_task
from functools import wraps
from math import ceil
from typing import Callable

from sqlalchemy import create_engine, select, orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from src.common.exceptions import MySQLError, ParamsError
from src.conf import settings


class DatabaseManager:
    """
    连接元数据库的类，在__init__中进行初始化
    """
    def __init__(self):
        # 第一步：创建一个AsyncEngine实例
        self._engine = create_async_engine(('mysql+aiomysql://{}:{}@{}:{}/{}'.format(
            settings.MYSQL_USER,
            settings.MYSQL_PASSWORD,
            settings.MYSQL_HOST,
            settings.MYSQL_PORT,
            settings.MYSQL_DATABASE,
            )), echo=True)

        self.session = None
        self.initialize()

    def initialize(self, scope_function: Callable = None):
        """
        Configure class for creating scoped sessions.
        """
        # Create the session factory classes
        # 第二步：创建一个工厂，确保每个session都通过Engine链接资源
        async_session_factory = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        # 第三步：session非线程安全，它是一个全局对象，次方法是确保线程本地化（在单线程中使用同一个session）
        self.session = async_scoped_session(async_session_factory, scopefunc=current_task)

    def cleanup(self):
        """
        Cleans up the database connection pool.
        """
        if self._engine is not None:
            self._engine.dispose()


@contextlib.asynccontextmanager
async def create_session() -> Session:
    db = DatabaseManager()
    session = db.session
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise MySQLError
    finally:
        await session.close()


def provide_session(func):
    """
    Function decorator that provides a session if it isn't provided.
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        arg_session = 'session'

        func_params = func.__code__.co_varnames
        session_in_args = arg_session in func_params and \
            func_params.index(arg_session) < len(args)
        session_in_kwargs = arg_session in kwargs
        if session_in_kwargs or session_in_args:
            return await func(*args, **kwargs)
        else:
            async with create_session() as session:
                kwargs[arg_session] = session
                return await func(*args, **kwargs)

    return wrapper


# SYNC
class SyncDatabaseManager:
    """
    连接元数据库的类，在__init__中进行初始化
    """
    def __init__(self):
        # 第一步：创建一个AsyncEngine实例
        self._engine = create_engine(('mysql+pymysql://{}:{}@{}:{}/{}'.format(
            settings.MYSQL_USER,
            settings.MYSQL_PASSWORD,
            settings.MYSQL_HOST,
            settings.MYSQL_PORT,
            settings.MYSQL_DATABASE,
            )), echo=True, future=True)

        self._session = None
        self.initialize()

    def initialize(self):
        self._session = scoped_session(sessionmaker(bind=self._engine))

    @property
    def session(self):
        return self._session


@contextlib.contextmanager
def sync_session():
    db = SyncDatabaseManager()
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise MySQLError
    finally:
        db.session.close()


if __name__ == '__main__':
    from models.users import Merchant
    with sync_session() as session:
        data = session.query(Merchant).filter(Merchant.id == 1).first()
        print(dir(data))






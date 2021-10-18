# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:58
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from conf import settings
# 初始化数据库连接
engine = create_async_engine('mysql+aiomysql://{}:{}@{}:{}/{}'.format(
    settings.MYSQL_HOST,
    settings.MYSQL_PORT,
    settings.MYSQL_USER,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_DATABASE)
)

SessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


async def get_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50), nullable=False)
    age = Column(Integer, nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all()


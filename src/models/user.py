# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/19 15:32
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.orm.query import Query

from connector.mysql_connector import create_session
from models.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50), nullable=False)
    age = Column(Integer, nullable=False)

    @classmethod
    async def get_user_info(cls, *args, **kwargs):

        print(kwargs)
        async with create_session() as session:
            result: AsyncResult = await session.execute(select(cls).limit(int(kwargs.get('page_size'))).offset(((int(kwargs.get('page')) - 1)) * int(kwargs.get('page'))))
            data = result.scalars().all()
        return data
# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:58
from datetime import datetime
from typing import Any

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base

from src.common.exceptions import ParamsError

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment='ID')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')


# 分页
class Pagination:

    def __call__(self, **kwargs):
        if not kwargs.get('page') or not kwargs.get('page_size'):
            page = int(kwargs.get('page'))
            page_size = int(kwargs.get('page_size'))
            if page <= 0 or page_size <= 0:
                raise ParamsError
            return ...
        else:
            raise ParamsError


if __name__ == '__main__':
    a = {'page': 10, 'page_size': 10}
    print(Pagination())











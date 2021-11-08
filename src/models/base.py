# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:58
import functools
from datetime import datetime
from typing import Any, List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base


from src.common.exceptions import ParamsError

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment='ID')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')


# 分页装饰器
def pagination(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        data: List = func(*args, **kwargs)
        page = kwargs.get('page', None)
        page_size = kwargs.get('page_size', None)
        if page is None or page_size is None:
            raise ParamsError
        if int(page) <= 0 or int(page_size) <= 0:
            raise ParamsError
        return data[page_size * (int(page - 1)) + 1: page_size * page + 1]
    return inner














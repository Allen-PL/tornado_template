# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:58
import functools
import json
from math import ceil
from time import strftime, localtime
from typing import List, Dict, Any

import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, Boolean, DateTime, func, text, inspect
from sqlalchemy.ext.declarative import declarative_base

from connector.mysql_connector import sync_session
from src.common.exceptions import ParamsError, ApiException, TokenError

Base = declarative_base()


# # 分页装饰器
# def pagination(func):
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         data = func(*args, **kwargs)
#         page = kwargs.get('page', None)
#         page_size = kwargs.get('page_size', None)
#         if page is None or page_size is None:
#             raise ParamsError
#         if int(page) <= 1 or int(page_size) <= 0:
#             raise ParamsError
#         # return data[page_size * (int(page - 1)) + 1: page_size * page + 1]
#         return data.limit(page_size).offset((page - 1) * page_size).all()
#     return inner


class CRUDMixin(object):
    """Mixin 添加CRUD操作: create, get(read), update, delete"""

    @classmethod
    def get_pk(cls, **kwargs):
        """查询某条数据是佛存在，返回pk"""
        with sync_session() as session:
            return session.query(cls).filter_by(**kwargs).first().id

    @classmethod
    def get(cls, **kwargs) -> object:
        """查询单条数据"""
        with sync_session() as session:
            return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_all(cls, **kwargs) -> List:
        """查询条件所有"""
        with sync_session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def all(cls):
        """获取表多有"""
        with sync_session() as session:
            return session.query(cls).all()

    @classmethod
    def add(cls, **kwargs):
        """新增一条或多条"""
        instance = cls()
        for attr, value in kwargs.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        with sync_session() as session:
            return session.add(instance)

    @classmethod
    def get_list(cls, data, condition=None):
        """获取分页数据"""
        if condition is None:
            condition = {}
        page = data.get('page') or None
        page_size = data.get('page_size') or None
        if page is None or page_size is None:
            raise ParamsError()
        if int(page) < 1 or int(page_size) <= 0:
            raise ParamsError()
        with sync_session() as session:
            return session.query(cls).filter_by(**condition).limit(page_size).offset((int(page) - 1) * int(page_size)).all()

    @classmethod
    def update(cls, old_pk: int, **kwargs):
        """更新"""
        # TODO 这里应该防止kwargs存在数据库中已有的字段
        data = {}
        for attr, value in kwargs.items():
            if hasattr(cls, attr):
                data[attr] = value
        with sync_session() as session:
            return session.query(cls).filter_by(id=old_pk).update(data)

    @classmethod
    def delete(cls, old_pk: int):
        """硬删除"""
        with sync_session() as session:
            return session.query(cls).filter_by(id=old_pk).delete()


class JSONSerializerMixin(object):

    @classmethod
    def serializer(cls, data: Any, is_dict=False):
        """
        :param data: [object, ...] or obejct or {}
        :param is_dict:
        :return:
        """
        fields_list = []
        if not is_dict:
            for obj in cls.__table__.columns.values():
                fields_list.append(obj.key)

        else:
            pass



class BaseModel(Base, CRUDMixin, JSONSerializerMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment='ID')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')






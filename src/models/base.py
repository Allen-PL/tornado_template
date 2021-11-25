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

from src.connector.mysql_connector import sync_session, create_session
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
    def objects_to_dict(cls, objects) -> [List, Dict]:
        result_dict = []
        print(objects)
        if isinstance(objects, List):
            for o in objects:
                element = {}
                for c in cls.__table__.columns:
                    element[c.name] = getattr(o, c.name)
                result_dict.append(element)
            return result_dict
        else:
            return {c.name: getattr(objects, c.name) for c in cls.__table__.columns}

    @classmethod
    def get_one(cls, **kwargs) -> object:
        """查询单条数据"""
        with sync_session() as session:
            return cls.objects_to_dict(session.query(cls).filter_by(**kwargs).first())

    @classmethod
    def get_all(cls, **kwargs) -> List:
        """查询条件所有"""
        with sync_session() as session:
            return cls.objects_to_dict(session.query(cls).filter_by(**kwargs).all())

    @classmethod
    def pagination(cls, data, condition=None):
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
            return cls.objects_to_dict(session.query(cls).filter_by(**condition).limit(page_size).offset(
                (int(page) - 1) * int(page_size)).all())

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
    def update(cls, old_instance: Dict, **kwargs):
        """更新"""
        # TODO 这里应该防止kwargs存在数据库中已有的字段
        data = {}
        for attr, value in kwargs.items():
            if hasattr(cls, attr):
                data[attr] = value
        with sync_session() as session:
            return session.query(cls).filter_by(id=old_instance.get('id').update(data))

    @ classmethod
    def delete(cls, old_instance: Dict):
        """硬删除"""
        with sync_session() as session:
            return session.query(cls).filter_by(id=old_instance.get('id')).delete()


class AsyncCURDMixin:
    """
        # 增
        result = await Merchant.async_add(new_data)
        print(result)
        # 改
        # old_instance = await session.get(Merchant, 8)
        # result = await Merchant.async_update(8, {'phone': '12345678910'})
        # print(result)
        # 删
        result = await Merchant.async_delete(8)
        print(result)
    """

    @classmethod
    async def async_add(cls, data: Dict):
        """新增一条或多条"""
        instance = cls()
        async with create_session() as session:
            for k, v in data.items():
                setattr(instance, k, v)
            session.add(instance)
            return await session.commit()

    @classmethod
    async def async_update(cls, pk: int, data: Dict):
        """更新"""
        async with create_session() as session:
            old_instance = await session.get(cls, pk)
            for k, v in data.items():
                setattr(old_instance, k, v)
            return await session.commit()

    @classmethod
    async def async_delete(cls, pk):
        """硬删除"""
        async with create_session() as session:
            old_instance = await session.get(cls, pk)
            await session.delete(old_instance)
            return await session.commit()


class JSONSerializerMixin(object):
    """
    目前只支持单张表的序列化，因为本项目中多有的表都是端关联的，所以设计多张表的情况，到时候就手动进行处理
    """

    def serializer(self, data: [Dict, List]):
        """
        :param data: [{}, ...] or {}
        :return:
        """
        setattr(self, 'origin_data', data)
        return self

    def get_display(self, fields: List, t: str):
        origin_data = getattr(self, 'origin_data')
        model_fields = [c.name for c in self.__table__.columns]

        for field in fields:
            if field.key not in model_fields:
                assert '请检查get_display()方法中参数是否存在于数据库表中'
            if t == 'str':
                # 类型转化，母线只有一个，后面可以都在这里进行扩展
                if isinstance(field.type, DateTime):
                    for data in origin_data:
                        data[field.key] = data.get(field.key).strftime('%Y-%m-%d %H:%M:%S')
            elif t == 'choice':
                pass
        return self

    def alias(self):
        # 替换键名
        pass

    def exclude(self, fields: List) -> [List, Dict]:
        # 判定链式调用此方法的必须是serializer
        real_exclude_fields = []
        model_fields = [c.name for c in self.__table__.columns]
        for field in fields:
            if field not in model_fields:
                continue
            real_exclude_fields.append(field)
        origin_data = getattr(self, 'origin_data')
        if isinstance(origin_data, List):
            for i in range(len(origin_data)):
                for del_field in real_exclude_fields:
                    origin_data[i].pop(del_field)
        elif isinstance(origin_data, Dict):
            for del_field in real_exclude_fields:
                origin_data.pop(del_field)
        return self

    def show(self, fields: List) -> [List, Dict]:
        real_exclude_field = model_fields = [c.name for c in self.__table__.columns]
        for field in fields:
            if field not in model_fields:
                continue
            real_exclude_field.remove(field)
        origin_data = getattr(self, 'origin_data')
        if isinstance(origin_data, List):
            for i in range(len(origin_data)):
                for del_field in real_exclude_field:
                    origin_data[i].pop(del_field)
        elif isinstance(origin_data, Dict):
            for del_field in real_exclude_field:
                origin_data.pop(del_field)
        return self

    @property
    def data(self):
        return getattr(self, 'origin_data')


class BaseModel(Base, JSONSerializerMixin, AsyncCURDMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment='ID')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @classmethod
    def clean_data(cls, data: Dict, exclude: List = None, fields: List = None) -> Dict:
        """
        清洗self.data中的字段，用于插入数据库
        :param fields:
        :param exclude:
        :param data: self.data
        :return:
        """
        new_data = {}
        if exclude and fields:
            raise ValueError("Cant's exist at the same time `exclude` and `fields` for clean_data")
        data_keys = set(data.keys())
        if exclude and isinstance(fields, List):
            data_keys = data_keys - set(exclude)
        elif fields and isinstance(fields, List):
            data_keys = data_keys & set(fields)
        for field in set(cls.__table__.columns.keys()) & data_keys:
            new_data[field] = data.get(field)
        return new_data







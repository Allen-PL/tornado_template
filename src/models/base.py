# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:58
import functools
import json
from datetime import datetime
from math import ceil
from time import strftime, localtime
from typing import Any, List

import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, Boolean, DateTime, func, text, inspect
from sqlalchemy.cprocessors import to_str
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

from connector.mysql_connector import sync_session
from src.common.exceptions import ParamsError

Base = declarative_base()

#
# # 分页懒加载
# class Pagination(object):
#     """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
#     can also construct it from any other SQLAlchemy query object if you are
#     working with other libraries.  Additionally it is possible to pass `None`
#     as query object in which case the :meth:`prev` and :meth:`next` will
#     no longer work.
#     """
#
#     def __init__(self, query, page, per_page, total, items):
#         #: the unlimited query object that was used to create this
#         #: pagination object.
#         self.query = query
#         #: the current page number (1 indexed)
#         self.page = page
#         #: the number of items to be displayed on a page.
#         self.per_page = per_page
#         #: the total number of items matching the query
#         self.total = total
#         #: the items for the current page
#         self.items = items
#
#     @property
#     def pages(self):
#         """The total number of pages"""
#         if self.per_page == 0:
#             pages = 0
#         else:
#             pages = int(ceil(self.total / float(self.per_page)))
#         return pages
#
#     def prev(self, error_out=False):
#         """Returns a :class:`Pagination` object for the previous page."""
#         assert self.query is not None, 'a query object is required ' \
#                                        'for this method to work'
#         return self.query.paginate(self.page - 1, self.per_page, error_out)
#
#     @property
#     def prev_num(self):
#         """Number of the previous page."""
#         if not self.has_prev:
#             return None
#         return self.page - 1
#
#     @property
#     def has_prev(self):
#         """True if a previous page exists"""
#         return self.page > 1
#
#     def next(self, error_out=False):
#         """Returns a :class:`Pagination` object for the next page."""
#         assert self.query is not None, 'a query object is required ' \
#                                        'for this method to work'
#         return self.query.paginate(self.page + 1, self.per_page, error_out)
#
#     @property
#     def has_next(self):
#         """True if a next page exists."""
#         return self.page < self.pages
#
#     @property
#     def next_num(self):
#         """Number of the next page"""
#         if not self.has_next:
#             return None
#         return self.page + 1
#
#     def iter_pages(self, left_edge=2, left_current=2,
#                    right_current=5, right_edge=2):
#         """Iterates over the page numbers in the pagination.  The four
#         parameters control the thresholds how many numbers should be produced
#         from the sides.  Skipped page numbers are represented as `None`.
#         This is how you could render such a pagination in the templates:
#
#         .. sourcecode:: html+jinja
#
#             {% macro render_pagination(pagination, endpoint) %}
#               <div class=pagination>
#               {%- for page in pagination.iter_pages() %}
#                 {% if page %}
#                   {% if page != pagination.page %}
#                     <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
#                   {% else %}
#                     <strong>{{ page }}</strong>
#                   {% endif %}
#                 {% else %}
#                   <span class=ellipsis>…</span>
#                 {% endif %}
#               {%- endfor %}
#               </div>
#             {% endmacro %}
#         """
#         last = 0
#         for num in range(1, self.pages + 1):
#             if num <= left_edge or \
#                     (self.page - left_current - 1 < num < self.page + right_current) or \
#                     num > self.pages - right_edge:
#                 if last + 1 != num:
#                     yield None
#                 yield num
#                 last = num
#
#
# # 参考flask_sqlalchemy的BaseQuery
# class BaseQuery(orm.Query):
#
#     def paginate(self, data=None, page=None, page_size=None, error_out=True, max_per_page=None):
#         """Returns ``per_page`` items from page ``page``.
#
#         If ``page`` or ``per_page`` are ``None``, they will be retrieved from
#         the request query. If ``max_per_page`` is specified, ``per_page`` will
#         be limited to that value. If there is no request or they aren't in the
#         query, they default to 1 and 20 respectively.
#
#         When ``error_out`` is ``True`` (default), the following rules will
#         cause a 404 response:
#
#         * No items are found and ``page`` is not 1.
#         * ``page`` is less than 1, or ``per_page`` is negative.
#         * ``page`` or ``per_page`` are not ints.
#
#         When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
#         1 and 20 respectively.
#
#         Returns a :class:`Pagination` object.
#         """
#         if data:
#             if page is None:
#                 try:
#                     page = int(data.get('page', 1))
#                 except (TypeError, ValueError):
#                     page = 1
#
#             if page_size is None:
#                 try:
#                     page_size = int(data.get('page_size', 20))
#                 except (TypeError, ValueError):
#                     page_size = 20
#         else:
#             if page is None:
#                 page = 1
#
#             if page_size is None:
#                 page_size = 20
#
#         if max_per_page is not None:
#             page_size = min(page_size, max_per_page)
#
#         if page < 1:
#             page = 1
#
#         if page_size < 0:
#             page_size = 20
#
#         items = self.limit(page_size).offset((page - 1) * page_size).all()
#
#         if not items and page != 1 and error_out:
#             raise ParamsError
#
#         total = self.order_by(None).count()
#
#         return Pagination(self, page, page_size, total, items)
#
#
# # # 分页装饰器
# # def pagination(func):
# #     @functools.wraps(func)
# #     def inner(*args, **kwargs):
# #         data: List = func(*args, **kwargs)
# #         page = kwargs.get('page', None)
# #         page_size = kwargs.get('page_size', None)
# #         if page is None or page_size is None:
# #             raise ParamsError
# #         if int(page) <= 0 or int(page_size) <= 0:
# #             raise ParamsError
# #         return data[page_size * (int(page - 1)) + 1: page_size * page + 1]
# #
# #     return inner
#
#
# class Query(BaseQuery):
#
#     def values_list(self, *col_names, flat=False):
#         """模仿django的values_list, 使用这个方法后直接执行了sql, 必须在结尾使用"""
#         res = list(self)
#         if len(res) == 0:
#             return []
#         ret = []
#         for r in res:
#             tmp = []
#             for idx, col in enumerate(col_names):
#                 # 只取第一个字段
#                 if flat:
#                     if isinstance(r, tuple):
#                         ret.append(r[0])
#                     else:
#                         ret.append(getattr(r, col))
#                     break
#                 else:
#                     if isinstance(r, tuple):
#                         tmp.append(r[idx])
#                     else:
#                         tmp.append(getattr(r, col))
#             if not flat:
#                 ret.append(tuple(tmp))
#         return ret
#
#     def values_dict(self, *col_names):
#         res = list(self)
#         ret = []
#         for r in res:
#             tmp = {}
#             for idx, col in enumerate(col_names):
#                 if isinstance(r, tuple):
#                     tmp[col] = r[idx]
#                 else:
#                     tmp[col] = getattr(r, col)
#             ret.append(tmp)
#         return ret
#
#     def filter_by(self, **kwargs):
#         if hasattr(self.statement.columns, 'delete_time') and 'delete_time' not in kwargs.keys():
#             kwargs['delete_time'] = None
#         return super(Query, self).filter_by(**kwargs)
#
#     def get_or_404(self, ident, e=None, error_code=None, msg=None):
#         rv = self.get(ident)  # 查询主键
#         if not rv:
#             ...
#         return rv
#
#     def first_or_404(self, e=None, error_code=None, msg=None):
#         """
#         :param e: 异常(exception)
#         :param error_code: 错误码
#         :param msg: 错误信息
#         :return:
#         """
#         rv = self.first()
#         if not rv:
#             ...
#         return rv
#
#     def all(self):
#         rv = list(self)  # TODO cls.query.filter_by(**kwargs) -> self， 所以self是一个理论上的query对象
#         return rv if len(rv) != 0 else []
#
#     def all_or_404(self, e=None, error_code=None, msg=None):
#         rv = self.all()
#         if not rv:
#             ...
#         return rv
#
#     def all_by_wrap(self, wrap='items'):
#         rv = self.all()
#         return {wrap: rv} if wrap else rv
#
#     def paginate(self, page=None, page_size=None, error_out=True, max_per_page=None):
#         """
#         :return:
#         :param page:页码，从1开始
#         :param page_size: 每页显示的记录数
#         :param error_out: 错误标记(如果是True，如果接收到超出记录范围的页面请求则报错；False则返回空列表)
#         :param max_per_page:
#         :return:
#         """
#         # 使用paginator记的加上filter_by，用于默认添加status=1
#         paginator = super(Query, self).paginate(page=page, page_size=page_size, error_out=error_out,
#                                                 max_per_page=max_per_page)
#         return Pagination(self,
#                           paginator.page,
#                           paginator.per_page,
#                           paginator.total,
#                           paginator.items
#                           )
#
#
# class CRUDMixin(object):
#     """Mixin 添加CRUD操作: create, get(read), update, delete"""
#
#     @classmethod
#     def get(cls, **kwargs):
#         """查询"""
#         print(type(cls))
#         return cls.query.filter_by(**kwargs).first()
#
#     @classmethod
#     def get_or_404(cls, e: Exception = None, error_code: int = None, msg: str = None, **kwargs):
#         """查询，不存在则返回异常"""
#         error_kwargs = dict(e=e, error_code=error_code, msg=msg)
#         return cls.query.filter_by(**kwargs).first_or_404(**error_kwargs)
#
#     @classmethod
#     def get_all(cls, **kwargs):
#         """查询所有"""
#
#         return cls.query.filter_by(cls, **kwargs).all()
#
#     @classmethod
#     def create(cls, commit: bool = True, **kwargs):
#         """新增"""
#         instance = cls()
#         for attr, value in kwargs.items():
#             if hasattr(instance, attr):
#                 setattr(instance, attr, value)
#         return instance.save(commit)
#
#     def update(self, commit: bool = True, **kwargs):
#         """更新"""
#         for attr, value in kwargs.items():
#             if hasattr(self, attr):
#                 setattr(self, attr, value)
#         return self.save(commit)
#
#     def save(self, commit: bool = True):
#         """保存"""
#         with sync_session as session:
#             session.add(self)
#         return self
#
#     def delete(self, commit: bool = True):
#         """硬删除"""
#         with sync_session as session:
#             result = session.delete(self)
#         return commit and result
#
#
# class JSONSerializerMixin(object):
#
#     @orm.reconstructor
#     def init_on_load(self):
#         # 被隐藏的属性则无法用append方法添加
#         self._locked = False  # ctrl(业务逻辑)层对字段hide和append的操作结束后，锁定
#         self._locked_fields = []  # 在业务逻辑处理中，锁住的字段
#         self._exclude = []
#         self._set_fields()  # 由子类重置exclude属性
#         self.__prune_fields()  # 初始化字段列表，按需裁剪
#
#     def lock_fields(self):
#         # ctrl(业务逻辑)层对字段锁定
#         self._locked = True
#
#     def _set_fields(self):
#         pass
#
#     def __prune_fields(self):
#         all_columns = inspect(self.__class__).columns.keys()  # 该model的所有属性
#         self.fields = list(set(all_columns) - set(self._exclude))
#
#     def keys(self):
#         """
#         __getitem__和keys 与dict有关;
#         item是由key中来的, 因此序列化可控
#         JSONEncoder, 会对查询结果dict化;
#         JSONSerializerMixin对字段的hide和append处理在「业务逻辑处理」之后
#         """
#         return self.fields
#
#     def __getitem__(self, item):
#         attr = getattr(self, item)
#         # 将字符串转为JSON
#         if isinstance(attr, str):
#             try:
#                 attr = json.loads(attr)
#             except ValueError:
#                 pass
#         # 处理时间(时间戳转化)
#         if item in ['create_time', 'update_time', 'delete_time']:
#             attr = strftime('%Y-%m-%d %H:%M:%S', localtime(attr))
#         return attr
#
#     def hide(self, *keys):
#         for key in keys:
#             if hasattr(self, key):
#                 if not self._locked:
#                     # 已经锁定的字段在keys中无法再删除
#                     self._locked_fields.append(key)
#                     self.fields.remove(key) if key in self.fields else None
#
#                 # 已经锁住，就不能在对ctrl操作hide和append过的字段，进行操作
#                 if self._locked and key not in self._locked_fields:
#                     self.fields.remove(key)
#         return self
#
#     def append(self, *keys):
#         for key in keys:
#             if hasattr(self, key):
#                 if not self._locked:
#                     # 已经锁定的字段在keys中无法再添加
#                     self._locked_fields.append(key)
#                     self.fields.append(key) if key not in self.fields else None
#
#                 # 已经锁住，就不能在对ctrl操作hide和append过的字段，进行操作
#                 if self._locked and key not in self._locked_fields:
#                     self.fields.append(key)
#         return self
#
#     def set_attrs(self, **kwargs):
#         # 快速赋值，用法: set_attrs(form.data)
#         for key, value in kwargs.items():
#             if hasattr(self, key) and key != 'id':
#                 setattr(self, key, value)
#
#
# class Model(object):
#     """Base class for SQLAlchemy declarative base model.
#
#     To define models, subclass :attr:`db.Model <SQLAlchemy.Model>`, not this
#     class. To customize ``db.Model``, subclass this and pass it as
#     ``model_class`` to :class:`SQLAlchemy`.
#     """
#
#     #: Query class used by :attr:`query`. Defaults to
#     # :class:`SQLAlchemy.Query`, which defaults to :class:`BaseQuery`.
#     query_class = None
#
#     #: Convenience property to query the database for instances of this model
#     # using the current session. Equivalent to ``db.session.query(Model)``
#     # unless :attr:`query_class` has been changed.
#     query = Query
#
#     def __repr__(self):
#         identity = inspect(self).identity
#         if identity is None:
#             pk = "(transient {0})".format(id(self))
#         else:
#             pk = ', '.join(to_str(value) for value in identity)
#         return '<{0} {1}>'.format(type(self).__name__, pk)
#
#
# class _QueryProperty(object):
#     def __init__(self, sa):
#         self.sa = sa
#
#     def __get__(self, obj, type):
#         try:
#             mapper = orm.class_mapper(type)
#             if mapper:
#                 return type.query_class(mapper, session=self.sa.session())
#         except Exception:
#             pass
#
# class BindMetaMixin(type):
#     def __init__(cls, name, bases, d):
#         bind_key = (
#             d.pop('__bind_key__', None)
#             or getattr(cls, '__bind_key__', None)
#         )
#
#         super(BindMetaMixin, cls).__init__(name, bases, d)
#
#         if bind_key is not None and getattr(cls, '__table__', None) is not None:
#             cls.__table__.info['bind_key'] = bind_key
#
#
# class NameMetaMixin(type):
#     def __init__(cls, name, bases, d):
#         if should_set_tablename(cls):
#             cls.__tablename__ = camel_to_snake_case(cls.__name__)
#
#         super(NameMetaMixin, cls).__init__(name, bases, d)
#
#         # __table_cls__ has run at this point
#         # if no table was created, use the parent table
#         if (
#             '__tablename__' not in cls.__dict__
#             and '__table__' in cls.__dict__
#             and cls.__dict__['__table__'] is None
#         ):
#             del cls.__table__
#
#     def __table_cls__(cls, *args, **kwargs):
#         """This is called by SQLAlchemy during mapper setup. It determines the
#         final table object that the model will use.
#
#         If no primary key is found, that indicates single-table inheritance,
#         so no table will be created and ``__tablename__`` will be unset.
#         """
#         # check if a table with this name already exists
#         # allows reflected tables to be applied to model by name
#         key = _get_table_key(args[0], kwargs.get('schema'))
#
#         if key in cls.metadata.tables:
#             return sa.Table(*args, **kwargs)
#
#         # if a primary key or constraint is found, create a table for
#         # joined-table inheritance
#         for arg in args:
#             if (
#                 (isinstance(arg, sa.Column) and arg.primary_key)
#                 or isinstance(arg, sa.PrimaryKeyConstraint)
#             ):
#                 return sa.Table(*args, **kwargs)
#
#         # if no base classes define a table, return one
#         # ensures the correct error shows up when missing a primary key
#         for base in cls.__mro__[1:-1]:
#             if '__table__' in base.__dict__:
#                 break
#         else:
#             return sa.Table(*args, **kwargs)
#
#         # single-table inheritance, use the parent tablename
#         if '__tablename__' in cls.__dict__:
#             del cls.__tablename__
#
#
# class DefaultMeta(NameMetaMixin, BindMetaMixin, DeclarativeMeta):
#     pass
#
#
#
# class SQLAlchemy:
#
#     def __init__(self, model_class=Model, query_class=BaseQuery):
#         self.Query = query_class
#         self.Model = self.make_declarative_base(model_class)
#
#     def make_declarative_base(self, model, metadata=None):
#         """Creates the declarative base that all models will inherit from.
#         :param model: base model class (or a tuple of base classes) to pass
#             to :func:`~sqlalchemy.ext.declarative.declarative_base`. Or a class
#             returned from ``declarative_base``, in which case a new base class
#             is not created.
#         :param metadata: :class:`~sqlalchemy.MetaData` instance to use, or
#             none to use SQLAlchemy's default.
#
#         .. versionchanged 2.3.0::
#             ``model`` can be an existing declarative base in order to support
#             complex customization such as changing the metaclass.
#         """
#         if not isinstance(model, DeclarativeMeta):
#             model = declarative_base(
#                 cls=model,
#                 name='Model',
#                 metadata=metadata,
#                 metaclass=DefaultMeta
#             )
#
#         # if user passed in a declarative base and a metaclass for some reason,
#         # make sure the base uses the metaclass
#         if metadata is not None and model.metadata is not metadata:
#             model.metadata = metadata
#
#         if not getattr(model, 'query_class', None):
#             model.query_class = self.Query
#
#         model.query = _QueryProperty(self)
#         return model




class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment='ID')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')






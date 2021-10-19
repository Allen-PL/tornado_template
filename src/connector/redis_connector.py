# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:13
import pickle
from typing import Any

from aioredis import ConnectionPool, Redis

from conf import settings


class BaseCache:
    key_prefix = settings.REDIS_PREFIX
    default_time_out = settings.REDIS_EXPIRE_TIME

    def __init__(self):
        self.client = self.client()

    @classmethod
    async def get_redis_pool(cls) -> ConnectionPool:
        if not hasattr(cls, '_redis_pool'):
            cls._redis_pool = ConnectionPool.from_url(
                "redis://{}:{}@{}:{}/{}".format(
                    settings.REDIS_USER,
                    settings.REDIS_PASSWORD,
                    settings.REDIS_HOST,
                    settings.REDIS_PORT,
                    max_connections=10)
            )
        return cls._redis_pool

    @classmethod
    async def client(cls) -> Redis:
        if not hasattr(cls, '_client'):
            cls._client = await Redis(connection_pool=cls.get_redis_pool())
        return cls._client

    # @classmethod
    # async def dump_object(cls, value) -> bytes:
    #     """Dumps an object into a string for redis.  By default it serializes
    #     integers as regular string and pickle dumps everything else.
    #     """
    #     t = type(value)
    #     if t == int:
    #         return str(value).encode("ascii")
    #     return b"!" + pickle.dumps(value)
    #
    # @classmethod
    # def load_object(cls, value: bytes) -> Any:
    #     """The reversal of :meth:`dump_object`.  This might be called with
    #     None.
    #     """
    #     if value is None:
    #         return None
    #     if value.startswith(b"!"):
    #         try:
    #             return pickle.loads(value[1:])
    #         except pickle.PickleError:
    #             return None
    #     try:
    #         return int(value)
    #     except ValueError:
    #         # before 0.8 we did not have serialization.  Still support that.
    #         return value
    #
    # # @classmethod
    # # def get_by_pk(cls, pk, model: Type[M]) -> M:
    # #     # 从缓存中获取, 如果没有就从数据库种读取, 并放到缓存
    # #     key = '{}::pk::{}'.format(model.__name__, pk)
    # #     data = cls.get(key)
    # #     if not data:
    # #         try:
    # #             data = model.objects.get(pk=pk)
    # #             cls.set(key, data)
    # #         except model.DoesNotExist:
    # #             data = None
    # #     return data
    #
    # @classmethod
    # def set_by_instance(cls, instance: M, model: Type[M]):
    #     """添加缓存"""
    #     key = '{}::pk::{}'.format(model.__name__, str(instance.id))
    #     cls.set(key, instance)
    #
    # @classmethod
    # def delete_by_pk(cls, pk, model: Type[M]):
    #     """删除"""
    #     key = '{}::pk::{}'.format(model.__name__, pk)
    #     return cls.delete(key)
    #
    # @classmethod
    # def delete(cls, key):
    #     """根据键删除"""
    #     return cls.strict_delete(cls.get_key_with_prefix(key))
    #
    # @classmethod
    # async def get(cls, key):
    #     """获取并解码"""
    #     return cls.load_object(cls.strict_get(cls.get_key_with_prefix(key)))
    #
    # @classmethod
    # async def set(cls, key, value, timeout=None):
    #     if timeout is None:
    #         timeout = cls.default_time_out
    #     dump = cls.dump_object(value)
    #     key_with_prefix = cls.get_key_with_prefix(key)
    #     if timeout == -1:
    #         result = cls.strict_set(key_with_prefix, value=dump)
    #     else:
    #         result = cls.strict_setex(key_with_prefix, value=dump, timeout=timeout)
    #     return result
    #
    # # 严格模式
    # @classmethod
    # def strict_get(cls, key):
    #     return cls.client().get(key)
    #
    @classmethod
    async def strict_set(cls, key, value):
        await cls.client().execute_command("set", key, value)
        # return cls.client().set(key, value=value)
    #
    # @classmethod
    # def strict_setex(cls, key, value, timeout):
    #     return cls.client().setex(key, value=value, time=timeout)
    #
    # @classmethod
    # def strict_delete(cls, key):
    #     return cls.client().delete(key)
    #
    # @classmethod
    # def get_key_with_prefix(cls, key):
    #     return '{}{}'.format(cls.key_prefix, key)
# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:13
import asyncio
import pickle
import traceback
from typing import Any

import aioredis
from aioredis import ConnectionPool, Redis
from tornado import gen

from common.exceptions import RedisError
from common.g import set_context
from conf import settings
from utils.web_log import get_logger


async def redis_async_connect(conn_time=None, retry_interval=5):
    """
    mongo的异步连接
        :param retry_interval: 重试间隔（单位：s）
        :param re_conn: 失败自动重连
        :param conn_time: 限制连接次数
        :return:
        """
    import motor
    __cnt = 0
    while True:
        try:
            if conn_time and __cnt == int(conn_time):
                get_logger().error('Mongodb async connect error,connect more than ' + str(conn_time) + ' times')
                raise RedisError

            pool = aioredis.Redis.from_url(
                    "redis://localhost",
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=10,
                )
            redis = await Redis(connection_pool=pool)
            get_logger().info('redis async connected successfully')
            # set_context(settings.G_REDIS_KEY, redis)
            return redis
        except Exception:
            __cnt += 1
            get_logger().exception('redis async connecting retry number: ' + str(__cnt))
            await gen.sleep(retry_interval)


class BaseCache:
    key_prefix = settings.REDIS_PREFIX
    default_time_out = settings.REDIS_EXPIRE_TIME

    async def get_eclient(self) -> Redis:
        if not hasattr(self, '_redis_pool'):
            self._redis_pool = ConnectionPool.from_url(
                "redis://{}:{}@{}:{}/{}".format(
                    settings.REDIS_USER,
                    settings.REDIS_PASSWORD,
                    settings.REDIS_HOST,
                    settings.REDIS_PORT,
                    settings.REDIS_DB,
                ),
                encoding="utf-8",
                decode_responses=True,
                max_connections=10,
            )
            self._client = await Redis(connection_pool=self._redis_pool)
        return self._client

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
    async def strict_set(self, key, value):
        try:
            a = (await self.get_eclient()).get('name')
            print(a)
        except Exception:
            print(traceback.print_exc())



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

# async def main():
#     # Redis client bound to single connection (no auto reconnection).
#     pool = aioredis.ConnectionPool.from_url(
#         "redis://localhost", encoding="utf-8", decode_responses=True
#     )
#     meanings = aioredis.Redis(connection_pool=pool)
#     await meanings.set()
#         await conn.set("name", "pl")
#         val = await conn.get("name")
#     print(val)


#
# if __name__ =='__main__':
#     asyncio.run(main())

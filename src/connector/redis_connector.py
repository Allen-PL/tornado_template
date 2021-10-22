# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:13
import asyncio
import pickle
from typing import Any

import aioredis
from aioredis import Redis

from conf import settings


class BaseCache:
    key_prefix = settings.REDIS_PREFIX
    default_time_out = settings.REDIS_EXPIRE_TIME

    @classmethod
    async def get_client(cls) -> Redis:
        cls._client = await aioredis.from_url(
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

    # @classmethod
    # async def load_object(cls, value: bytes) -> Any:
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

    @classmethod
    async def get_key_with_prefix(cls, key):
        return '{}::{}'.format(cls.key_prefix, key)

    # 解析方法
    @classmethod
    async def set(cls, key, value, timeout=None):
        if timeout is None:
            timeout = cls.default_time_out
        # dump = await cls.dump_object(value)
        key_with_prefix = await cls.get_key_with_prefix(key)
        if timeout == -1:
            result = await cls.strict_set(key_with_prefix, value)
        else:
            result = await cls.strict_setex(key_with_prefix, value, timeout=timeout)
        return result

    @classmethod
    async def get(cls, key):
        """获取并解码"""
        return await cls.strict_get(await cls.get_key_with_prefix(key))

    @classmethod
    async def delete(cls, key):
        """根据键删除"""
        return await cls.strict_delete(await cls.get_key_with_prefix(key))

    # 严格模式
    @classmethod
    async def strict_get(cls, key):
        cls.client = await cls.get_client()
        return await cls.client.get(key)

    @classmethod
    async def strict_set(cls, key, value):
        cls.client = await cls.get_client()
        return await cls.client.set(key, value)

    @classmethod
    async def strict_setex(cls, key, value, timeout):
        cls.client = await cls.get_client()
        return await cls.client.setex(key, value=value, time=timeout)

    @classmethod
    async def strict_delete(cls, key):
        cls.client = await cls.get_client()
        return await cls.client.delete(key)


if __name__ == '__main__':
    pass
    # print(asyncio.run(BaseCache().set('name', 'pl')))
    # print(asyncio.run(BaseCache().get('name')))
    # print(asyncio.run(BaseCache().delete('name')))
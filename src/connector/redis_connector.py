# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:13
import asyncio
import json
import pickle
from typing import Any

import aioredis
from aioredis import Redis

from conf import settings
from dao.merchant_dao import MerchantDao
from utils.web_log import get_logger


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
            encoding='utf-8',
            # decode_responses=True,  # 返回自动decode
            max_connections=10,
        )
        return cls._client

    @classmethod
    async def dump_object(cls, value) -> bytes:
        """Dumps an object into a string for redis.  By default it serializes
        integers as regular string and pickle dumps everything else.
        """
        t = type(value)
        if t == int:
            return str(value).encode("ascii")
        return pickle.dumps(value)

    @classmethod
    async def load_object(cls, value: bytes) -> Any:
        """The reversal of :meth:`dump_object`.  This might be called with
        None.
        """
        if value is None:
            return None
        try:
            return pickle.loads(value)
        except Exception as e:
            get_logger().error(f"功能：基础服务解析(aioredis) || 涉及方法：load_object || 异常信息：{e}")
            return None

    @classmethod
    async def get_key_with_prefix(cls, key):
        return '{}::{}'.format(cls.key_prefix, key)

    # 解析方法
    @classmethod
    async def set(cls, key, value, timeout=None):
        if timeout is None:
            timeout = cls.default_time_out
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

    @classmethod
    async def incr(cls, key) -> int:
        """自增"""
        return await cls.strict_incr(await cls.get_key_with_prefix(key))

    @classmethod
    async def ttl(cls, key) -> int:
        """获取过期时间"""
        return await cls.strict_ttl(key)

    @classmethod
    async def set_ttl(cls, key, timeout: int) -> bool:
        """设置建的过期时间"""
        return await cls.strict_set_ttl(key, timeout)

    @classmethod
    async def set_bytes(cls, key, instance: Any, timeout=None):
        return await cls.strict_set_bytes(key, instance, timeout=timeout)

    @classmethod
    async def get_bytes(cls, key):
        return await cls.strict_get_bytes(key)


########################## 严格模式  ######################


    @classmethod
    async def strict_get(cls, key):
        cls.client = await cls.get_client()
        return await cls.client.get(key)

    @classmethod
    async def strict_set(cls, key, value, timeout=None):
        cls.client = await cls.get_client()
        return await cls.client.set(key, value, ex=timeout)

    @classmethod
    async def strict_setex(cls, key, value, timeout):
        cls.client = await cls.get_client()
        return await cls.client.setex(key, value=value, time=timeout)

    @classmethod
    async def strict_delete(cls, key):
        cls.client = await cls.get_client()
        return await cls.client.delete(key)

    @classmethod
    async def strict_incr(cls, key):
        cls.client = await cls.get_client()
        return await cls.client.incr(key)

    @classmethod
    async def strict_ttl(cls, key):
        cls.client = await cls.get_client()
        return await cls.client.ttl(key)

    @classmethod
    async def strict_set_ttl(cls, key, timeout: int):
        cls.client = await cls.get_client()
        return await cls.client.expire(key, timeout)

    @classmethod
    async def strict_set_bytes(cls, key, mapping, timeout=None):
        cls.client = await cls.get_client()
        await cls.client.set(key, await cls.dump_object(mapping), ex=timeout)

    @classmethod
    async def strict_get_bytes(cls, key):
        cls.client = await cls.get_client()
        return await cls.load_object(await cls.client.get(key))


if __name__ == '__main__':
    # print(asyncio.run(BaseCache().strict_ttl('name')))
    # print(asyncio.run(BaseCache().get('name1')))
    # print(asyncio.run(BaseCache().delete('name')))
    # print(asyncio.run(BaseCache().strict_set_ttl('name', 200)))
    # merchant_instance = asyncio.run(MerchantDao.get_merchant_instance_by_phone('12345678911'))
    a = {
        'a': 'c',
        'b': '1'
    }
    # print(asyncio.run(BaseCache().strict_set_bytes('name', a)))
    print(asyncio.run(BaseCache().strict_get_bytes('name')))


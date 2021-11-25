# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 通用缓存，没有涉及到表的交互操作
# @Author: pl
# @Time: 2021/10/19 17:31
from typing import Dict, Any

from common.exceptions import CacheError
from connector.redis_connector import BaseCache

# TODO：异步模式下怎么保证缓存数据的一致性：做binlog事务补偿来解决（放到后面 有这个必要的时候再搞）


# Access frequency restriction
class AccessFrequencyCache(BaseCache):
    prefix = 'frequency::'

    async def set_login_access_frequency_by_phone(self, key, value: int, timeout=None):
        return await self.set(key, value, timeout=timeout)

    async def add_login_access_frequency_by_phone(self, key: str):
        return await self.incr(key)

    async def get_login_access_frequency_by_phone(self, key: str):
        return await self.get(key)

    async def get_ttl_by_phone(self, key: str):
        return await self.ttl(key)

    async def set_ttl_by_phone(self, key, timeout):
        return await self.set_ttl(key, timeout)


# RefreshToken
class RefreshTokenCache(BaseCache):
    prefix = 'refresh_token::'

    async def set_refresh_token_by_phone(self, key, value, timeout: int):
        return await self.set(key, value, timeout)

    async def get_refresh_token_by_phone(self, key):
        return await self.get(key)




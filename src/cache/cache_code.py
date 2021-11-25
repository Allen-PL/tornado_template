# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/23 11:23
from typing import Any

from common.exceptions import CacheError
from connector.redis_connector import BaseCache


class CodeCache(BaseCache):

    prefix = 'code::'
    flag_prefix = 'code::flag'

    def __init__(self, prefix=None):

        if prefix:
            self.prefix = prefix

    async def set_code(self, key: str, value: str, timeout=None):
        return await self.set(self.prefix + key, value, timeout)

    async def get_code(self, key: str):
        return await self.get(key)

    async def delete_code(self, key: str) -> int:
        return await self.delete(key)

    async def set_code_request_expiration(self, key: str, value: Any, timeout=None):
        return await self.set(self.flag_prefix + key, value, timeout)

    async def get_code_request_expiration(self, key: str):
        return await self.get(key)

    async def delete_code_request_expiration(self, key: str) -> int:
        return await self.delete(key)






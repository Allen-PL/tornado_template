# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/19 17:31
from typing import Dict, Any

from common.exceptions import CacheError
from connector.redis_connector import BaseCache


class UserCache(BaseCache):

    prefix = 'user::'

    def __init__(self, prefix=None):

        if prefix:
            self.prefix = prefix

    async def set_user(self, key: str, value: Any):
        return await self.set(self.prefix + 'name', 'pl')

    async def get_user_by_pk(self, pk: str):
        user: Dict = await self.get(self.prefix + pk)
        if not user:
            try:
                # 查询数据库
                data = {
                    'name': 'pl',
                    'age': 18
                }
                result = await self.set_user(self.prefix + pk, data)
                if not await self.get(self.prefix + pk):
                    raise CacheError()
                return result
            except Exception as e:
                get_logger().exception(f'查询用户缓存信息异常，异常信息：{e}')
        return await self.get(self.prefix + pk)


class RoleCache(BaseCache):

    prefix = 'role::'

    pass


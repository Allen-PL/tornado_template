# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/24 10:52
import asyncio
from typing import Dict, List

from connector.redis_connector import BaseCache
from dao.merchant_dao import MerchantDao, MerchantRolesDao, MerchantPermissionsDao


class MerchantCache(BaseCache):
    prefix = 'merchant::'

    async def set_merchant_instance_by_phone(self, phone: str, instance):
        return await self.set_bytes(self.prefix + phone, instance)

    async def get_merchant_instance_by_phone(self, phone: str) -> Dict:
        instance = await self.get_bytes(self.prefix + phone)
        if not instance:
            instance = await MerchantDao.get_merchant_instance_by_phone(phone)
            await self.set_merchant_instance_by_phone(phone, instance)
        return instance


# Note：角色和权限的缓存都使用id作为键，这样可以减少一个mysql数据库查询
class MerchantRolesCache(BaseCache):
    prefix = 'merchant_roles::'

    async def set_merchant_roles_instance_by_uid(self, uid: int, instances, timeout=None):
        return await self.set_bytes(self.prefix + str(uid), instances, timeout)

    async def get_merchant_roles_instance_by_uid(self, uid: int):
        """
        [instance, instance...]
        """
        roles_instance = await self.get_bytes(self.prefix + str(uid))
        if roles_instance:
            return roles_instance
        roles_instance = await MerchantRolesDao.get_merchant_roles_instances_by_uid(uid)
        await self.set_merchant_roles_instance_by_uid(self.prefix + str(uid), roles_instance)
        return roles_instance


class MerchantPermissionsCache(BaseCache):
    prefix = 'merchant_permissions::'

    async def set_merchant_permissions_instance_by_uid(self, uid: int, instances, timeout=None):
        return await self.set_bytes(self.prefix + str(uid), instances, timeout)

    async def get_merchant_permissions_instance_by_uid(self, uid: int):
        permissions_instance = await self.get_bytes(self.prefix + str(uid))
        if permissions_instance:
            return permissions_instance
        permissions_instance = await MerchantPermissionsDao.get_merchant_permissions_instance_by_uid(uid)
        await self.set_merchant_permissions_instance_by_uid(uid, permissions_instance)
        return permissions_instance




if __name__ == '__main__':
    result = asyncio.run(MerchantCache().get_merchant_instance_by_phone('12345678911'))
    print(result)



# class UserCache(BaseCache):
#
#     prefix = 'user::'
#
#     def __init__(self, prefix=None):
#
#         if prefix:
#             self.prefix = prefix
#
#     async def set_user(self, key: str, value: Any):
#         return await self.set(self.prefix + 'name', 'pl')
#
#     async def get_user_by_pk(self, pk: str):
#         user: Dict = await self.get(self.prefix + pk)
#         if not user:
#             try:
#                 # 查询数据库
#                 data = {
#                     'name': 'pl',
#                     'age': 18
#                 }
#                 result = await self.set_user(self.prefix + pk, data)
#                 if not await self.get(self.prefix + pk):
#                     raise CacheError()
#                 return result
#             except Exception as e:
#                 get_logger().exception(f'查询用户缓存信息异常，异常信息：{e}')
#         return await self.get(self.prefix + pk)


# class RoleCache(BaseCache):
#
#     prefix = 'role::'
#
#     pass
# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/24 11:01
import asyncio
from typing import Dict, List

from sqlalchemy import select, and_

from models.users import Merchant, MerchantRole, MRole, Permission, MRolePermission
from src.connector.mysql_connector import provide_session


class MerchantDao:

    @classmethod
    @provide_session
    async def get_merchant_exists_by_phone(cls, phone, session=None) -> bool:
        result = await session.execute(select(Merchant.id).where(Merchant.phone == phone))
        return False if not result.first() else True

    @classmethod
    async def create_merchant(cls, data: Dict):
        # 清晰数据 -> 入库
        await Merchant.async_add(Merchant.clean_data(data, fields=['phone', 'password', 'avatar', 'no', 'department',
                                                                   'company', 'postbox', 'grade']))

    @classmethod
    @provide_session
    async def get_merchant_instance_by_phone(cls, phone, session=None) -> Merchant:
        result = await session.execute(select(Merchant).where(Merchant.phone == phone))
        return result.scalar()


class MerchantRolesDao:

    @classmethod
    @provide_session
    async def get_merchant_roles_instances_by_uid(cls, u_id, session=None) -> List[MRole]:
        middle_instance = await session.execute(
            select(MerchantRole.r_id).where(MerchantRole.u_id == u_id, MerchantRole.status == True))
        result = await session.execute(select(MRole).filter(MRole.id.in_(middle_instance.scalars())))
        return result.scalars()


class MerchantPermissionsDao:

    @classmethod
    @provide_session
    async def get_merchant_permissions_instance_by_uid(cls, u_id, session=None) -> List[Permission]:
        roles_middle_instance = await session.execute(
            select(MerchantRole.r_id).where(MerchantRole.u_id == u_id, MerchantRole.status == True))
        permissions_middle_instance = await session.execute(
            select(MRolePermission.p_id).where(MRolePermission.r_id.in_([r_id for r_id in roles_middle_instance.scalars()]), MRolePermission.status == True))
        result = await session.execute(select(Permission).filter(Permission.id.in_(permissions_middle_instance.scalars())))
        return result.scalars()


if __name__ == '__main__':
    for i in asyncio.run(MerchantPermissionsDao().get_merchant_permissions_instance_by_uid(1)):
        print(i)

# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/5 13:41
from typing import Dict

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncResult


from models.users import Merchant
from src.constants.table import EnumUserStatus, EnumUserMark, EnumRoleType
from src.connector.mysql_connector import create_session, DatabaseManager, provide_session, sync_session
from models.base import pagination


class UsersDao():

    @classmethod
    def get_merchant_by_phone(cls, **kwargs) -> bool:
        with sync_session() as session:
            return session.query(Merchant.phone == kwargs.get('phone')).count()

    @classmethod
    def add_merchant(cls, **kwargs) -> Dict:
        with sync_session() as session:
            data = session.add(Merchant(phone=kwargs.get('phone'), password=kwargs.get('password')))
            print(data.phone)

        return {
            'name': 'pl'
        }

    @classmethod
    @pagination
    def get_merchant(cls, **kwargs):
        with sync_session() as session:
            data = session.query(Merchant).filter(Merchant.id >= 1)

            print('data:', data.count())

            return data


if __name__ == '__main__':
    data = UsersDao.get_merchant(**{
        'page': 1,
        'page_size': 10
    })
    # 装饰器返回
    # print('======data:', data[0].phone)


    #     data = {
    #         'phone': str(i),
    #         'password': str(i)
    #     }
    #     result = UsersDao.add_merchant(**data)
    #     print(result)

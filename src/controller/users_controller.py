# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/4 14:28
from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncResult

from models.users import Merchant
from src.constants.table import EnumUserStatus, EnumUserMark, EnumRoleType
from src.connector.mysql_connector import create_session, DatabaseManager, provide_session


class UsersController:

    @provide_session
    def merchant_register(self, session=None, **kwargs) -> Dict:
        data = session.execute(select(Merchant).where(id==1))
        print(data)


        return {
            'name': 'pl'
        }


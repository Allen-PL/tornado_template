# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:20
# from utils.authenticated import login_authentication
import time

import tornado
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.base_handler import BaseHandler
from common.exceptions import ApiException
from models.user import User
from utils.cache_set import UserCache
from utils.web_log import get_logger


class MainHandler(BaseHandler):

    # @login_authentication
    async def get(self):
        # 走校验，将校验后的参数也封装进data中，到时候只传入校验后的数据
        # data = await User.get_user_info(**self.data)
        # for i in data:
        #     print(i.name)
        await UserCache.strict_set('name', 'pl')

        return self.response_data(info='ok')

    def post(self):
        print(self.data.get('name'))
        return self.response_data()

    def put(self):
        return self.response_data('ok')




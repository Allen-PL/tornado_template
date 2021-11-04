# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:20
# from utils.authenticated import login_authentication
import time
from typing import Optional, Awaitable

import tornado
from aioredis import ConnectionPool, Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tornado import web

from common.authenlication import user_login
from conf import settings
from connector.redis_connector import BaseCache
from handlers.base_handler import BaseHandler
from common.exceptions import ApiException, AuthenticationError
from utils.cache_set import UserCache
from utils.web_log import get_logger
from validation import BaseValidation, NotNull, Past, NotEmpty, Size


class MainHandler(BaseHandler):

    # @user_login
    def get(self):
        # 走校验，将校验后的参数也封装进data中，到时候只传入校验后的数据
        # data = await User.get_user_info(**self.data)
        # for i in data:
        #     print(i.name)
        # user_cache = UserCache()
        # print(self.data)
        # BaseValidation.valid_data(
        #     self.data,
        #     {
        #         'num1': [NotEmpty(), Size(1, 10)],
        #         'num2': [NotEmpty(), Size(1, 10)],
        #     }
        # )
        # result = await user_cache.get_user_by_pk('1')

        return self.response_data(info='ok')

    def post(self):
        print(self.data.get('name'))
        return self.response_data()

    def put(self):
        return self.response_data('ok')







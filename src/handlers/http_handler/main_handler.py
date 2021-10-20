# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:20
# from utils.authenticated import login_authentication
import time

import tornado
from aioredis import ConnectionPool, Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conf import settings
from connector.redis_connector import redis_async_connect, BaseCache
from handlers.base_handler import BaseHandler
from common.exceptions import ApiException
from models.user import User
from utils.cache_set import UserCache
from utils.web_log import get_logger


async def get_redis_pool():
    _redis_pool = ConnectionPool.from_url(
        "redis://{}:{}@{}:{}/{}".format(
            settings.REDIS_USER,
            settings.REDIS_PASSWORD,
            settings.REDIS_HOST,
            settings.REDIS_PORT,
            settings.REDIS_DB),
        encoding="utf-8", decode_responses=True
    )
    connect = Redis(connection_pool=_redis_pool)
    return connect


class MainHandler(BaseHandler):

    # @login_authentication
    async def get(self):
        # 走校验，将校验后的参数也封装进data中，到时候只传入校验后的数据
        # data = await User.get_user_info(**self.data)
        # for i in data:
        #     print(i.name)

        # (await redis_async_connect()).set('name2', 'pl2')

        await BaseCache().strict_set('name2', 'pl2')

        return self.response_data(info='ok')

    def post(self):
        print(self.data.get('name'))
        return self.response_data()

    def put(self):
        return self.response_data('ok')




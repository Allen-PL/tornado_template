# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:20
# from utils.authenticated import login_authentication
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.base_handler import BaseHandler
from common.exceptions import ApiException
from models.base import get_db_session, User
from utils.web_log import get_logger


class MainHandler(BaseHandler):

    # @login_authentication
    async def get(self, db_session: AsyncSession = get_db_session):
        async with db_session.begin():
            results = await get_db_session().execute(select(User).limit(10))
        data = results.scalars().all()
        print(data)
        return self.response_data(data)

    def post(self):
        print(self.data.get('name'))
        return self.response_data()

    def put(self):
        return self.response_data('ok')


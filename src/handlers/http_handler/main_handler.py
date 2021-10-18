# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:20
# from utils.authenticated import login_authentication

from handlers.base_handler import BaseHandler
from common.exceptions import ApiException
from utils.web_log import get_logger


class MainHandler(BaseHandler):

    # @login_authentication
    def get(self):
        a = 1
        a[0]
        get_logger().exception("123456789123456798")
        info = {'name': 'mast be a int'}
        return self.response_data(info)

    def post(self):
        print(self.data.get('name'))
        return self.response_data()

    def put(self):
        return self.response_data('ok')

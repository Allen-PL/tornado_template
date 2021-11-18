# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/25 11:06
import functools
import re

from tornado.web import RequestHandler


# TODO 认证需要同步，否则数据是否会发生紊乱
from common.exceptions import AuthenticationError
from conf import settings
from utils.auth_util import token_to_user
from utils.web_log import get_logger


def user_login(func):
    @functools.wraps(func)
    def wrapper(  # type: ignore
            self, *args, **kwargs):
        self.data['user'] = None
        for url in settings.WHITE_LIST:
            if re.match(self.request.path, url):
                return None
        token = self.data.get('access_token')
        if token:
            try:
                user = token_to_user(token)
                self.data['user'] = user
            except Exception as e:
                get_logger().exception(f'initialize认证异常：token解析失败，异常原因： {e}')
                return self.response_data(*AuthenticationError().os)
        else:
            get_logger().exception('initialize认证异常：token未传，登录认证失败!')
            return self.response_data(*AuthenticationError().os)
        return func(self, *args, **kwargs)
    return wrapper

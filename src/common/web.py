# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 10:01
import json
import re
import traceback

from tornado import web, websocket, gen

from common.exceptions import ApiException, DataTypeError, AuthenticationError, ParamsError
from conf import settings
from utils.auth_util import token_to_user
from utils.web_log import get_logger


class HttpBasicHandler(web.RequestHandler):

    def set_default_headers(self):
        # 无论是否跨域，都预设如下response_header，在调试或者线上均可用
        self.set_header("Access-Control-Expose-Headers", "Content-Disposition")
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get('Origin') or "*")
        self.set_header('Access-Control-Allow-Credentials', "true")

    @property
    def data(self):
        # 获取url 和 body中的参数
        argument_data = dict()
        a = self.request.query_arguments
        for i in a.keys():
            argument_data[i] = self.get_argument(i)
        if self.request.body:
            body_data = json.loads(self.request.body.decode('utf-8'))
            if isinstance(body_data, dict):
                body_data.update(argument_data)
                return body_data
            else:
                get_logger().exception('body data is not a dict')
                raise DataTypeError()
        # 获取headers中的access_token参数，data['access_token'] = None
        elif self.request.headers.get('access_token'):
            argument_data['access_token'] = self.request.headers.get('access_token') or None
        else:
            return argument_data

    # 重写web的钩子，每次请求都会执行
    def initialize(self):
        '''
        TODO 这个钩子里面不能抛出任何异常
        def _initialize(self) -> None:
            pass
        '''
        raise ParamsError
        # print(self.request.path)
        # for url in settings.WHITE_LIST:
        #     if re.match(self.request.path, url):
        #         return None
        # token = self.data.get('access_token')
        # print('----------token:', token)
        #
        # if token:
        #     try:
        #         user, token = token_to_user(token)
        #     except Exception as e:
        #         get_logger().exception(f'token解析异常，异常原因： {e}')
        #         raise AuthenticationError()
        # else:
        #     user, token = None, None
        #     raise AuthenticationError()
        # setattr(self.data, 'user', user)
        # setattr(self.data, 'token', token)





    def response_data(self, code=200, msg='请求成功', info=None):
        result = {
            'code': code,
            'msg': msg,
            'info': info
        }
        try:
            self.finish(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.finish(json.dumps(ApiException(info=str(e)).os, ensure_ascii=False))
            traceback.print_exc()


class WebsocketBasicHandler(websocket.WebSocketHandler):
    pass






# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 10:01
import json
import re
import traceback
import datetime
from typing import Optional, Awaitable

from tornado import web, websocket, gen

from common.exceptions import ApiException, DataTypeError, AuthenticationError, ParamsError, NotFoundError, TokenError
from conf import settings
from utils.auth_util import token_to_user
from utils.sign import check_sign
from utils.web_log import get_logger


class HttpBasicHandler(web.RequestHandler):

    def get(self):
        raise NotFoundError()

    def set_default_headers(self):
        # 无论是否跨域，都预设如下response_header，在调试或者线上均可用
        self.set_header("Access-Control-Expose-Headers", "Content-Disposition")
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get('Origin') or "*")
        self.set_header("Access-Control-Allow-Credentials", "true")

    # 在执行http请求之前调用，框架初始化自定义内容的钩子
    def initialize(self):
        # 这里打印请求的一些信息
        if settings.DEBUG:
            request_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            request_url = self.request.full_url()
            print(f"\033[33m{request_time}\033[0m" + " --> " + f"\033[36m{request_url}\033[0m")

    # 超类建议实现的方法，可以忽略
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    # 在执行对应的请求方法之前调用
    def prepare(self):
        # 视图之前的钩子，用来校验post、put、delete时sign是否合法
        if self.request.method.upper() in ['POST', 'PUT', 'DELETE']:
            check_sign(self.request.body)  # 只对body里面的参数进行合法性校验
        # 在视图之前实现认证校验
        self.auth_middleware()

    @property
    def data(self):
        # 参数一：获取url 和 body中的参数
        data = dict()
        a = self.request.query_arguments
        for i in a.keys():
            data[i] = self.get_argument(i)
        if self.request.body:
            body_data = json.loads(self.request.body.decode('utf-8'))
            if isinstance(body_data, dict):
                body_data.update(data)
                return body_data
            else:
                get_logger().exception('body data is not a dict')
                raise DataTypeError()
        # 参数二：获取headers中的access_token参数，data['access_token'] = None
        elif self.request.headers.get('access_token'):
            data['access_token'] = self.request.headers.get('access_token') or None
        elif self.request.headers.get('refresh_token'):
            data['refresh_token'] = self.request.headers.get('refresh_token') or None
        else:
            return data

    def response_data(self, info=' ', code=200, msg='请求成功'):
        result = {
            'code': code,
            'msg': msg,
            'info': info
        }
        try:
            self.finish(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            result['code'] = ApiException().code
            result['msg'] = ApiException().msg
            result['info'] = str(e)
            self.finish(json.dumps(result))
            traceback.print_exc()

    # 实现认证中间件
    def auth_middleware(self):
        token = self.request.headers.get('access_token')
        # 跳过白名单
        is_excluded = False
        for url in settings.ACCESS_WHITELIST:
            # 如果当前url匹配到排除列表，不理会
            if url.match(self.request.path):
                is_excluded = True
                break
        if is_excluded:
            return
        # 解析token
        try:
            if token:
                # 获取请求的用户
                user = token_to_user(token)
                setattr(self.data, '_user', user)
                return
        except Exception as e:
            get_logger().exception(f'功能：解析token || 状态：失败 || 失败原因：{e}')
            raise AuthenticationError()
        raise TokenError()


class WebsocketBasicHandler(websocket.WebSocketHandler):
    pass






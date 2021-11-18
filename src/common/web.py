# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 10:01
import json
import re
import traceback
from typing import Optional, Awaitable

from tornado import web, websocket, gen

from common.exceptions import ApiException, DataTypeError, AuthenticationError, ParamsError
from conf import settings
from utils.auth_util import token_to_user
from utils.sign import check_sign
from utils.web_log import get_logger


class HttpBasicHandler(web.RequestHandler):

    def set_default_headers(self):
        # 无论是否跨域，都预设如下response_header，在调试或者线上均可用
        self.set_header("Access-Control-Expose-Headers", "Content-Disposition")
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get('Origin') or "*")
        self.set_header("Access-Control-Allow-Credentials", "true")

    # 超类建议实现的方法，可以忽略
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    # 视图之前的钩子，用来校验post、put、delete时sign是否合法
    def prepare(self):
        if self.request.method.upper() in ['POST', 'PUT', 'DELETE']:
            check_sign(self.data)

    @property
    def data(self):
        # 获取url 和 body中的参数
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
        # 获取headers中的access_token参数，data['access_token'] = None
        elif self.request.headers.get('access_token'):
            data['access_token'] = self.request.headers.get('access_token') or None
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


class WebsocketBasicHandler(websocket.WebSocketHandler):
    pass






# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 10:01
import json
import traceback

from tornado import web, websocket

from common.exceptions import ApiException, DataTypeError
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
        print(self.request.path)
        # for url in WHITE_LIST:
        #     if url.match(self.request.path):
        #         return None
        # token = self.data.get('access_token')
        # try:
        #     if token:
        #         user, token = token_to_user(token)
        #     else:
        #         user, token = None, None
        #     setattr(self.data, 'user', user)
        #     setattr(self.data, 'token', token)
        # except Exception as e:
        #     access_log(f'token解析异常，异常原因： { e }')

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






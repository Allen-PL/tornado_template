# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/14 16:05
import traceback

from common.exceptions import ApiException
from common.web import HttpBasicHandler
from utils.web_log import get_logger


class BaseHandler(HttpBasicHandler, ApiException):

    def options(self):
        self.set_status(200)
        self.finish()

    def write_error(self, status_code, **kwargs):
        """
        统一异常响应处理
        :param status_code:
        :param kwargs:
        :return:
        """
        print('异常捕获到了...........................')
        # 统一记录下500的错误, 这里可以填写出错后返回的信息
        exc_cls, exc_instance, trace = kwargs.get("exc_info")
        print(exc_cls, exc_instance, trace)
        # 只处理500的错误
        if status_code == 500:

            get_logger().error(traceback.format_exception(exc_cls, exc_instance, trace))
            # 自定义异常抛400
            if isinstance(exc_instance, ApiException):
                self.set_status(400)
                return self.response_data(code=exc_instance.code, msg=exc_instance.msg, info=exc_instance.info)
            # 系统未知异常抛500
            self.set_status(status_code)
            return self.response_data(*(ApiException().os))

    def set_default_headers(self):
        """添加返回content-type是json的标识符, 方便postman调试"""
        super().set_default_headers()
        self.set_header('Access-Control-Allow-Methods', 'PUT,DELETE,OPTIONS,GET,POST')
        self.set_header("Content-Type", "application/json; charset=utf-8")



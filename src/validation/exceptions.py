""" 
@Function:
@Author  : ybb
@Time    : 2020/9/28 18:10
"""
from common.exceptions import ParamsError


class ValidException(ParamsError):
    """自定义校验异常"""
    def __init__(self, info=None, msg='字段校验错误'):
        super().__init__(msg)
        self.info = info
        self.msg = msg


class FieldValidException(ParamsError):
    """自定义字段校验异常"""
    def __init__(self, msg='字段校验错误'):
        super().__init__(msg)
        self.msg = msg

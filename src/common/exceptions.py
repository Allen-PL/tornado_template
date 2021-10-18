# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/14 16:07

class ApiException(Exception):
    code = 1000
    msg = '系统异常'
    info = None

    def __init__(self, code=None, msg=None, info=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if info:
            self.info = info

    @property
    def os(self):
        return {'code': self.code, 'msg': self.msg, 'info': self.info}


# ************ HTTP ERROR **********
class ParamsError(ApiException):
    code = 1001
    msg = '参数错误'


class TokenError(ApiException):
    code = 1002
    msg = "未登录"


class AuthorityError(ApiException):
    code = 1003
    msg = "无权限"


class NotFoundError(ApiException):
    code = 1004
    msg = '无此项目'


class TimeError(ApiException):
    code = 1005
    msg = "敬请期待"


class StatusError(ApiException):
    code = 1006
    msg = '状态有误'


class DataTypeError(ApiException):
    code = 1007
    msg = '数据类型错误'


# ************ OS INNER EXCEPTION ***********
class OSInnerError(ApiException):
    msg = '系统内部异常'


class MongoDBError(OSInnerError):
    pass


class MySQLError(OSInnerError):
    pass


class RedisError(OSInnerError):
    pass


class RabbitmqError(OSInnerError):
    pass


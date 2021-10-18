# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:11

from conf.base import VERSION
from handlers.http_handler.main_handler import MainHandler


urls = [
    (VERSION + '/', MainHandler),
]

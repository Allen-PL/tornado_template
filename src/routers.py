# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/15 9:11
import tornado

from conf import settings
from handlers.base_handler import BaseHandler
from handlers.http_handler.login_handler import LoginHandler, RefreshTokenHandler
from handlers.http_handler.main_handler import MainHandler
from handlers.http_handler.register_handler import RegisterHandler, CodeHandler


urls = [
    # Notice：url参数按照驼峰的形势命名
    (settings.VERSION + '/', MainHandler),
    (settings.VERSION + '/smscode/', CodeHandler),
    (settings.VERSION + '/merchant/register/', RegisterHandler),
    (settings.VERSION + '/merchant/login/', LoginHandler),
    (settings.VERSION + '/merchant/refreshToken/', RefreshTokenHandler),

]

# 404NotFound处理
urls += [('.*', BaseHandler)]


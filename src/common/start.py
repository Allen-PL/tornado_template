# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 11:00
from tornado import web, ioloop

from conf import settings
from routers import urls
from utils.web_log import log_request


def start_precess_app():

    app = web.Application(
        handlers=urls,
        debug=settings.DEBUG,
        # log_function=log_request
    )

    app.listen(address=settings.APP_HOST, port=settings.APP_PORT)
    print("服务启动成功!")
    ioloop.IOLoop.current().start()
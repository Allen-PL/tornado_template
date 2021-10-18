# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 11:00
from tornado import web, ioloop

from conf import settings
from routers import urls


def start_precess_app():

    app = web.Application(
        handlers=urls,
        debug=settings.DEBUG,
    )
    app.listen(settings.APP_PORT, address=settings.APP_HOST)
    print("服务启动成功!")
    ioloop.IOLoop.current().start()
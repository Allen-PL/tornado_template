# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/14 17:55
import logging
from logging.handlers import TimedRotatingFileHandler

import tornado.log
from tornado.web import RequestHandler


# 日志消息格式（finish -> 走到这）
from common.common_log import DefaultLogger
from conf import settings


def log_request(handler: RequestHandler):

    if handler.get_status() < 400:
        log_method = tornado.log.access_log.info
    elif handler.get_status() < 500:
        log_method = tornado.log.access_log.warning
    else:
        log_method = tornado.log.access_log.error

    request_time = 1000.0 * handler.request.request_time()
    log_method("执行状态码：%d， 请求Origin：（%s）， 请求总耗时：%.2fms", handler.get_status(), handler._request_summary(), request_time)


def get_logger():
    return DefaultLogger.get_logger(settings.LOG_FULL_PATH, 1024 * 1024 * 10, 30)













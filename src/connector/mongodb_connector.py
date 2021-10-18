# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:14
from tornado import gen

from common.exceptions import MongoDBError
from common.g import set_context
from conf import settings
from utils.web_log import get_logger


async def mongodb_connect(conn_time=settings.MONGODB_CONN_TIME, retry_interval=5):
    """
    :param retry_interval: 重试间隔（单位：s）
    :param re_conn: 失败自动重连
    :param conn_time: 限制连接次数
    :return:
    """
    import pymongo
    __cnt = 0
    while True:
        try:
            if conn_time and __cnt == int(conn_time):
                get_logger().error('MongoDB connect error,connect more than' + str(conn_time) + 'times')
                raise MongoDBError
            mongodb_host = settings.MONGODB_HOST
            mongodb_port = int(settings.MONGODB_PORT)
            connector = pymongo.MongoClient(mongodb_host, mongodb_port)
            get_logger().info('mongodb connected successfully')
            set_context(settings.G_MONGODB_KEY, connector)
            return connector
        except Exception:
            __cnt += 1
            get_logger().exception('mongodb connecting retry number: ' + str(__cnt))
            await gen.sleep(retry_interval)


async def mongodb_async_connect(conn_time=None, retry_interval=5):
    """
        :param retry_interval: 重试间隔（单位：s）
        :param re_conn: 失败自动重连
        :param conn_time: 限制连接次数
        :return:
        """
    import motor
    __cnt = 0
    while True:
        try:
            if conn_time and __cnt == int(conn_time):
                get_logger().error('Mongodb async connect error,connect more than ' + str(conn_time) + ' times')
                raise MongoDBError
            mongodb_host = settings.MONGODB_HOST
            mongodb_port = int(settings.MONGODB_PORT)
            connector = motor.motor_tornado.MotorClient(mongodb_host, mongodb_port)
            get_logger().info('mongodb async connected successfully')
            set_context(settings.G_MONGODB_KEY, connector)
            return connector
        except Exception:
            __cnt += 1
            get_logger().exception('mongodb async connecting retry number: ' + str(__cnt))
            await gen.sleep(retry_interval)






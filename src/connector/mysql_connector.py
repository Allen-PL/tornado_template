# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 14:14
# from tornado import gen
#
# from common.exceptions import MySQLError
# from common.g import set_context
# from conf import settings
# from utils.web_log import get_logger
#
#
# async def mysql_async_connect(conn_time=settings.MYSQL_CONN_TIME, retry_interval=5):
#     import aiomysql
#     __cnt = 0
#     while True:
#         try:
#             if conn_time and __cnt == int(conn_time):
#                 get_logger().error('MySQL connect error,connect more than' + str(conn_time) + 'times')
#                 raise MySQLError
#             mysql_host = settings.MYSQL_HOST
#             mysql_port = settings.MYSQL_PORT
#             mysql_user = settings.MYSQL_USER
#             mysql_password = settings.MYSQL_PASSWORD
#             mysql_database = settings.MYSQL_DATABASE
#             conn = aiomysql.connect(
#                 host=mysql_host,
#                 port=mysql_port,
#                 user=mysql_user,
#                 password=mysql_password,
#                 db=mysql_database,
#             )
#             cur = await conn.cursor()
#
#
#
#             get_logger().info('mysql connected successfully')
#             set_context(settings.G_MYSQL_KEY, connector)
#             return connector
#         except Exception:
#             __cnt += 1
#             get_logger().exception('mysql connecting retry number: ' + str(__cnt))
#             await gen.sleep(retry_interval)






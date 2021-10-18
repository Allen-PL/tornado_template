# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:44
import os
import datetime

# ************************** APP CONF INFO ******************************

# APP BASIC INFO
APP_HOST = '127.0.0.1'
APP_PORT = 9999
DEBUG = True

# VERSION INFO
VERSION = '/api/v1'

# WHITE LIST
WHITE_LIST = ['']

# TOKEN CONF INFO
SECRET_KEY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
AUTH_SALT = 'chinaNB'
TOKEN_EXPIRATION = 60 * 60 * 24 * 7  # 默认设备过期时间7天

# ************************** LOG CONF INFO *****************************

LOG_FULL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs/{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d')))


# ************************** CONNECTOR CONF INFO ************************

# MySQL CONF INFO
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'empt'
MYSQL_CONN_TIME = 5
G_MYSQL_KEY = 'mysql_connector'

# MongoDB CONF INFO
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_CONN_TIME = 5
G_MONGODB_KEY = 'mongodb_connector'

# REDIS CONF INFO
REDIS_HOST = '127.0.0.1'
PORT = 6379
REDIS_CONN_TIME = 5
G_REDIS_KEY = 'redis_connector'


# RabbitMQ CONF INFO
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 16536
G_RABBITMQ_KEY = 'rabbitmq_connector'













# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:44
import logging
import os
import datetime

# ************************** APP CONF INFO ******************************
# COMMON SALT（make_password、check_password...）
COMMON_SALT = '6ijekanpnuy6'

# APP BASIC INFO
APP_HOST = '127.0.0.1'
APP_PORT = 8888
DEBUG = True

# VERSION INFO
VERSION = '/api/v1'

# WHITE LIST
WHITE_LIST = ['']

# ACCESS TOKEN CONF INFO
SECRET_KEY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
AUTH_SALT = 'chinaNB'
TOKEN_EXPIRATION = 60 * 60 * 24 * 7  # 默认token过期时间7天

# REFRESH TOKEN CONF INFO
REFRESH_TOKEN_EXPIRATION = 60 * 60 * 24 * 30  # 默认refresh_token的刷新时间为30天（必须比token的保质期长）
REFRESH_TOKEN_MAX_TIME = 3  # access token刷新最大的时间配置（单位：h）

# SMS VERIFICATION CODE
CODE_EXPIRATION = 300  # 验证码默认有效时间5min（300s）
CODE_REQUEST_EXPIRATION = 60  # 验证码的请求间隔时间默认1min（60s）

# FREQUENCY LIMIT
FREQUENCY = (60 * 60, 5)  # 默认5次/1h(密码输入错误时，在此有效期做计数)
FREQUENCY_LIMIT = 60 * 60 * 2  # 当用户输入密码的机会使用完，在此有效期内无法进行登录

# USERS DEFAULT AVATAR
USERS_DEFAULT_AVATAR = ['https://img1.jepg', 'https://img2.jepg', 'https://img3.jepg', 'https://img4.jepg'
                        'https://img5.jepg', 'https://img6.jepg', 'https://img7.jepg', 'https://img8.jepg']

# ACCESS WHITELIST(注册、登录、忘记密码)
ACCESS_WHITELIST = [VERSION + url for url in ('/merchant/register/', '/merchant/login/', '/forget/pwd/')]


# ************************** LOG CONF INFO *****************************
LOG_SIZE = 1024 * 1024 * 10
LOG_LEVEL = 'INFO'
LOG_FULL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs/{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d')))
LOG_BACK_COUNT = 30


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
REDIS_USER = ''
REDIS_PASSWORD = ''
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_CONN_TIME = 5
REDIS_PREFIX = 'empt'
REDIS_EXPIRE_TIME = -1
REDIS_DB = 0
G_REDIS_KEY = 'redis_connector'


# RabbitMQ CONF INFO
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 16536
G_RABBITMQ_KEY = 'rabbitmq_connector'













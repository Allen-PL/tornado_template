# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 11:36
import logging.config
from logging.handlers import RotatingFileHandler
from os.path import splitext, basename

from conf import settings


class DefaultLogger():
    standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'
    simple_format = '%(asctime)s %(message)s'

    @classmethod
    def get_logger(cls, log_level=settings.LOG_LEVEL, log_path=settings.LOG_FULL_PATH,
                   log_size=settings.LOG_SIZE, log_back_count=settings.LOG_BACK_COUNT):
        # log配置字典
        LOGGING_DIC = {
            'version': 1,
            'disable_existing_loggers': False,
            # 封装上面定义的日志格式
            'formatters': {
                'standard': {'format': cls.standard_format},
                'simple': {'format': cls.simple_format},
            },
            'handlers': {
                # 日志输出到终端
                'stream': {
                    'level': log_level,  # 输出到终端的级别
                    'class': 'logging.StreamHandler',  # 选择输出到终端的类
                    'formatter': 'simple'  # 输出的模式，是上面定义的
                },
                # 日志输出到文件
                'file': {
                    'level': log_level,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'filename': log_path,  # 输出的日志文件
                    'maxBytes': log_size,  # 单文件日志大小（最好不要设置太大）
                    'backupCount': log_back_count,  # 最多保存的日志文件个数
                    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                },
            },
            'loggers': {
                # logging.getLogger(__name__)拿到的logger配置
                '': {
                    'handlers': ['file', 'stream'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                    'level': 'INFO',
                    'propagate': True,  # 向上（更高level的logger）传递
                },
            },
        }
        # 导入上面定义的logging配置
        logging.config.dictConfig(LOGGING_DIC)
        # 生成一个log实例
        logger = logging.getLogger()
        return logger



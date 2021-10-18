# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 11:36
import logging
from logging.handlers import RotatingFileHandler
from os.path import splitext, basename


class DefaultLogger:
    logger = None

    @classmethod
    def get_logger(cls, log_path, log_size, log_num):
        if not cls.logger:
            cls.logger = logging.getLogger(splitext(basename(log_path))[0])
            cls.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s ' +
                                          ' %(name)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s')
            steam_handler = logging.StreamHandler()
            steam_handler.setFormatter(formatter)
            cls.logger.addHandler(steam_handler)

            if log_path:
                rotate_handler = RotatingFileHandler(log_path, maxBytes=log_size, backupCount=log_num)
                rotate_handler.setFormatter(formatter)
                cls.logger.addHandler(rotate_handler)
        return cls.logger
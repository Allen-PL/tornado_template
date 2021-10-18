# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/18 15:55
from typing import Any

from utils.web_log import get_logger


class InitConnector:
    context = {}


# ######### External Interface ######
def set_context(key: str, value):
    if key in InitConnector.context:
        get_logger().error('set key to context failed,' + str(key) + ' already exists')
        raise ValueError
    InitConnector.context[key] = value


def get_context(key: str) -> Any:
    if key in InitConnector.context:
        return InitConnector.context[key]
    return None


def update_context(key: str, value):
    InitConnector.context[key] = value
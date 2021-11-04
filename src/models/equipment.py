# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/1 15:56
from sqlalchemy import Column, Integer, String, select, Boolean, BigInteger, UniqueConstraint

from models.base import BaseModel


# 设备分类表
class EquipmentCate(BaseModel):
    ...
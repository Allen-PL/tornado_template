# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/22 12:00
from sqlalchemy import Column, Integer, String, Boolean

from src.models.base import Base


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50), nullable=False)
    age = Column(Integer, nullable=False)
    aex = Column(Boolean, default=1)
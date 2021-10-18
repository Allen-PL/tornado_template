# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 17:08
# 定义User对象:
from sqlalchemy import Column, String

from base import Base


class User(Base):
    # 表的名字:
    __tablename__  = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


if __name__ == '__main__':
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(sys.path)
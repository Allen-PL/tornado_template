# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/1 15:35
from sqlalchemy import Column, Integer, String

from models.base import BaseModel


class SMS(BaseModel):
    __tablename__ = '短信发送表'
    type = Column(Integer, default=..., comment='消息类型')
    content = Column(String(256), nullable=False, comment='消息主体内容')
    phone = Column(String(18), nullable=False, index=True, comment='接收消息手机号')
    response = Column(String(5), default='未响应', comment='响应状态码')
    code = Column(String(8), default='', comment='短信中附带的验证码')
    ipaddr = Column(String(32), default='0.0.0.0', comment='请求的ip地址')
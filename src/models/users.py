# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/19 15:32
from sqlalchemy import Column, String, Boolean, BigInteger, UniqueConstraint, DateTime, Integer
from sqlalchemy_utils import ChoiceType

from src.models.base import BaseModel


# #########################  管理员、角色   ##############################
# 管理员表
class Admin(BaseModel):
    __tablename__ = 'admin'
    phone = Column(String(18), unique=True, index=True, nullable=False, comment='手机号(用于登录)')
    password = Column(String(128), nullable=False, comment='密码')
    avatar = Column(String(256), nullable=False, comment='管理员头像')
    status = Column(Boolean, default=True, comment='账户状态')
    no = Column(String(32), nullable=False, comment='工号')
    department = Column(String(64), default='', index=True, comment='部门')
    last_time = Column(DateTime, nullable=True, comment='最后登录时间')
    ipaddr = Column(String(32), default='', comment='登录ip地址')
    postbox = Column(String(64), default='', comment='邮箱')
    superuser = Column(Boolean, default=False, comment='标记超级管理员')
    extra_field1 = Column(String(256), default='', comment='冗余字段1')
    extra_field2 = Column(String(256), default='', comment='冗余字段2')
    extra_field3 = Column(String(256), default='', comment='冗余字段3')
    extra_field4 = Column(String(256), default='', comment='冗余字段4')


# 管理员角色关联表
class AdminRole(BaseModel):
    __tablename__: str = 'pk_admin_role'
    u_id = Column(BigInteger, index=True, nullable=False, comment='管理员id')
    r_id = Column(BigInteger, index=True, nullable=False, comment='角色id')
    status = Column(Boolean, default=True, comment='用户角色关联状态')


# 角色表
class ARole(BaseModel):
    __tablename__ = 'arole'
    r_name = Column(String(32), nullable=False, unique=True, comment='角色名称')
    r_code = Column(String(32), nullable=False, unique=True, comment='角色代码')
    r_desc = Column(String(256), default='', comment='角色描述')
    r_status = Column(Boolean, default=True, comment='角色状态')


# #########################  商户、角色   ##############################
# 商户表
class Merchant(BaseModel):
    a = (
        (1, 'a'),
        (2, 'b')
    )
    __tablename__ = 'merchant'
    phone = Column(String(18), unique=True, index=True, nullable=False, comment='手机号(用于登录)')
    password = Column(String(128), nullable=False, comment='用于密码')
    avatar = Column(String(256), nullable=True, comment='用户头像')
    status = Column(Boolean, default=True, comment='账户状态')
    no = Column(String(32), nullable=True, comment='工号')
    department = Column(String(64), default='', index=True, comment='部门')
    last_time = Column(DateTime, nullable=True, comment='最后登录时间')
    ipaddr = Column(String(32), default='', comment='登录ip地址')
    company = Column(String(32), default='', comment='所属公司')
    postbox = Column(String(64), default='', comment='邮箱')
    extra_field1 = Column(String(256), default='', comment='冗余字段1')
    extra_field2 = Column(String(256), default='', comment='冗余字段2')
    extra_field3 = Column(String(256), default='', comment='冗余字段3')
    extra_field4 = Column(String(256), default='', comment='冗余字段4')


# 商户角色关联表
class MerchantRole(BaseModel):
    __tablename__: str = 'pk_merchant_role'
    u_id = Column(BigInteger, index=True, nullable=False, comment='商户id')
    r_id = Column(BigInteger, index=True, nullable=False, comment='角色id')
    status = Column(Boolean, default=True, comment='用户角色关联状态')


# 角色表
class MRole(BaseModel):
    __tablename__ = 'mrole'
    r_name = Column(String(32), nullable=False, unique=True, comment='角色名称')
    r_code = Column(String(32), nullable=False, unique=True, comment='角色代码')
    r_desc = Column(String(256), default='', comment='角色描述')
    r_status = Column(Boolean, default=True, comment='角色状态')


# ##########################  权限表   #############################
# 权限表
class Permission(BaseModel):
    __tablename__ = 'permission'
    p_name = Column(String(32), nullable=False, unique=True, comment='权限名称')
    P_code = Column(String(32), nullable=False, unique=True, comment='权限代码')
    uri = Column(String(128), nullable=False, comment='权限对应的uri')
    method = Column(String(12), nullable=False, comment='uri对应的方法')
    p_desc = Column(String(256), server_default='', comment='权限描述')
    p_status = Column(Boolean, default=True, comment='权限状态')
    p_type = Column(Boolean, nullable=False, comment='权限类型（标记内部人员独有的权限）')

    __table_args__ = (
        UniqueConstraint('uri', 'method', name='ix_uri_method'),
    )


# 商户角色权限关联表
class MRolePermission(BaseModel):
    __tablename__ = 'pk_merchant_role_permission'
    r_id = Column(BigInteger, nullable=False, index=True, comment='商户角色id')
    p_id = Column(BigInteger, nullable=False, index=True, comment='权限id')
    status = Column(Boolean, default=True, comment='角色权限关联状态')


# 管理员角色权限关联表
class ARolePermission(BaseModel):
    __tablename__ = 'pk_admin_role_permission'
    r_id = Column(BigInteger, nullable=False, index=True, comment='管理员角色id')
    p_id = Column(BigInteger, nullable=False, index=True, comment='权限id')
    status = Column(Boolean, default=True, comment='角色权限关联状态')


# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/14 13:46
import datetime
import time
import traceback
from functools import wraps
from typing import List, Set

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from conf import settings

# from django.conf import settings
# from web.cache.user_cache import UserCache, RoleCache
# from web.models.user import User
from models.users import Merchant
from utils.cache_set import UserCache, RoleCache

# ============= token加密与解密
from utils.web_log import get_logger


def user_to_token(user, expiration=None):
    """设置获取token"""
    if not expiration:
        expiration = settings.TOKEN_EXPIRATION
    s = Serializer(settings.SECRET_KEY, salt=settings.AUTH_SALT, expires_in=expiration)
    return s.dumps({
        'username': user.username,
        'id': user.id,
    }).decode()


def token_to_user(token):
    if not token:
        return None
    try:
        s = Serializer(settings.SECRET_KEY, salt=settings.AUTH_SALT)
        data = s.loads(token, return_header=True)[0]
        header = s.loads(token, return_header=True)[1]
        user_id = data.get('id')
        # token的剩余有效时间
        remaining_time = (header.get('exp') - time.time()) / 3600
        cache = UserCache()
        user = cache.get_user_by_pk(user_id)
        setattr(user, 'token', token)
        setattr(user, 'remaining_time', remaining_time)
        return user
    # 该模块提供的一些异常
    except BadSignature:
        get_logger().error('签名错误: {}'.format(token))
    except SignatureExpired:
        get_logger().error('过期token: {}'.format(token))
    except Exception:
        get_logger().error(traceback.format_exc())
    return None


# ============= 进入试图必须的角色权限


# def roles_required(*role_names):
#     """角色需求"""
#     def view_func(func):
#         @wraps(func)
#         def _wrapper(self, *args, **kargs):
#             user = self.request.user
#             if not user:
#                 raise TokenError()
#             if not role_names or has_roles(user, *role_names):
#                 print(has_roles(user, *role_names))
#                 return func(self, *args, **kargs)
#             raise AuthorityError()
#         return _wrapper
#     return view_func

# 辛苦了Thanks for your hard work
# def permissions_required(*permission_names, **kwargs):
#     """权限需求"""
#
#     def view_func(func):
#         write_log = kwargs.get('write_log', True)
#
#         @wraps(func)
#         def _wrapper(self, *args, **kwargs):
#             user = self.request.user
#             if write_log:
#                 logger.info({
#                     'path': self.request.path,
#                     'params': self.request.GET,
#                     # 'body': 'file data' if self.request.FILES else self.request.data,
#                     'body': 'file data' if self.request.FILES else b'',
#                     'method': self.request.method,
#                     'user': user,
#                     'ip': self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR'),
#                 })
#             if not user:
#                 raise TokenError()
#             if not user.is_active:
#                 raise TokenError('用户被禁用')
#             # 校验手机端不能登陆
#             # if not check_mobile_uuid(user.mobile_uuid):
#             #     """mobile_uuid（空返回True）"""
#             #     if 'Android' not in self.request.headers.get('User-Agent'):
#             #         raise AuthorityError('移动端没有访问权限')
#             if not permission_names:
#                 """登录就有访问权限"""
#                 return func(self, *args, **kwargs)
#             if has_permissions(user, *permission_names):
#                 return func(self, *args, **kwargs)
#             raise AuthorityError()
#
#         return _wrapper
#
#     return view_func


# ============= 是否拥有角色权限


# def has_roles(user: User, *role_name: str):
#     # 判断是否有某些角色
#     return set(role_name) & set(get_role_names(user))
#
#
# # 判断是否有权限
# def has_permissions(user: User, *permission_name: str):
#     permission_name_of_user = get_permissions(user)
#     if 'all' in permission_name_of_user:
#         # 超管用户: 拥有绝对权限
#         return True
#     return bool(set(permission_name) & permission_name_of_user)
#
# # ============= 获取角色权限
#
#
# def get_role_names(user) -> List[str]:
#     user_cache = UserCache()
#     return [x.role_name for x in user_cache.get_roles(user)]
#
#
# def get_permissions(user: User) -> Set[str]:
#     user_cache = UserCache()
#     role_cache = RoleCache()
#     # 基于角色查看权限
#     roles_of_user = user_cache.get_roles(user)
#     permission_name_of_user = set()
#     for role in roles_of_user:
#         permissions_name_of_role = role_cache.get_permissions_name(role.id)
#         permission_name_of_user.update(permissions_name_of_role)
#     return permission_name_of_user




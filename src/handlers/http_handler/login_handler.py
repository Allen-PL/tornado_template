# __*__coding:utf-8__*__
# @ModuleName: 登录功能、忘记密码功能
# @Function: LoginHandler、ForgetPsdHandler
# @Author: pl
# @Time: 2021/11/23 15:06
import uuid

from cache.cache_common import AccessFrequencyCache, RefreshTokenCache
from cache.cache_merchant import MerchantRolesCache, MerchantPermissionsCache
from common.exceptions import CustomizeError, ParamsError
from conf import settings
from dao.merchant_dao import MerchantDao, MerchantRolesDao
from handlers.base_handler import BaseHandler


# 限流操作：这里的限流目前采用手机号注册的次数来计算（放到cache）({'手机号': [第一次时间、第二次时间...]})
from utils.auth_util import merchant_to_token
from utils.utils import check_password
from utils.web_log import get_logger
from validation import BaseValidation, NotEmpty, IsPhone, Min


# 登录
class LoginHandler(BaseHandler):
    """
    TODO：目前的登录都是以手机号为基准，但是客户后面也有可能手机号不再使用了。这个时候就有两种解决方案：
    方案一：账号迁移（老的手机号迁移到新的手机号）
    方案二：提供其他的账号登录方式
    """
    async def post(self):
        role_cache = MerchantRolesCache()
        permissions_cache = MerchantPermissionsCache()
        frequency_cache = AccessFrequencyCache()
        validated_data = BaseValidation.valid_data(
            self.data,
            {
                'username': [NotEmpty(), IsPhone()],
                'password': [NotEmpty(), Min(8)]
            }
        )
        username = validated_data.validated_data.get('username')
        # 访问数据库之前检查是否备限流
        access_total = await frequency_cache.get_login_access_frequency_by_phone(username) or 0
        if access_total == settings.FREQUENCY[-1]:
            expiration = await frequency_cache.get_ttl_by_phone(username)
            expiration = 0 if expiration < 0 else expiration
            m, s = divmod(expiration, 60)
            h, m = divmod(m, 60)
            raise CustomizeError(msg=f'您的账号已经锁定，请{h}小时{m}分钟{s}秒之后再操作')
        merchant_instance = await MerchantDao.get_merchant_instance_by_phone(validated_data.validated_data.get('username'))
        if not merchant_instance:
            raise CustomizeError('用户不存在')
        verified = check_password(validated_data.validated_data.get('password', ''), merchant_instance.password)
        if not verified:
            # 错误次数缓存累加（用做限流凭证，防止账号频繁的访问，如果是恶意访问的，我觉得就在nginx层面做黑名单防护）
            # 第 1 次
            if not access_total:
                await frequency_cache.set_login_access_frequency_by_phone(username, 1, timeout=settings.FREQUENCY[0])
            # 第 2 到第 n - 1 次
            elif access_total < settings.FREQUENCY[-1] - 1:
                await frequency_cache.add_login_access_frequency_by_phone(username)
            # 第 n 次
            else:
                await frequency_cache.set_login_access_frequency_by_phone(username, settings.FREQUENCY[-1], timeout=settings.FREQUENCY_LIMIT)
            raise CustomizeError(f'密码错误，你还有{settings.FREQUENCY[-1] - access_total + 1}次机会')
        # 校验用户状态是否备禁用
        if not merchant_instance.status:
            raise CustomizeError('用户已被禁用')
        # 生成token
        token = merchant_to_token(merchant_instance)

        # 缓存角色、权限(TODO 角色、权限返回、封装格式序列化还是得做)
        roles_instance = await role_cache.get_merchant_roles_instance_by_uid(merchant_instance.id)
        permissions_instance = await permissions_cache.get_merchant_permissions_instance_by_uid(merchant_instance.id)

        # 更新数据库


        # 返回组装数据

        # 记录日志

        #


        return self.response_data('ok')


        # role_ids = Role.objects.filter(user__pk=user.id).values('id')
        # print(role_ids)
        # result = {
        #     'username': user.username,
        #     'name': user.display,
        #     'token': token,
        #     'refresh_token': refresh_token,
        #     'roles': get_role_names(user),
        #     'permissions': get_permissions(user)
        # }
        # login_time = datetime.now()
        # login_ip = request.headers.get('Host', None)
        # platform = request.headers.get('platform', None)
        # if not platform or platform not in settings.PLATFORM:
        #     raise ParamsError('platform参数缺失')
        # data = {'login_time': login_time, 'login_ip': login_ip, 'platform': platform, 'user': user.pk}
        # instance = UserLoginInfo.objects.filter(user=user.id).first()
        # if instance:
        #     serializer = UserLoginInfoSerializer(instance=instance, data=data)
        # else:
        #     serializer = UserLoginInfoSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # log_data = {
        #     'operator': user.username,
        #     'type': 'login',
        #     'desc': f'用户<{user.username}>登入系统,登录IP：<{get_client_ip(request)}>'
        # }
        # add_operation_log(log_data)
        # logger.info((data, log_data))
        # self.cache.delete_by_pk(user.id, User)
        # return Success(result)



class RefreshTokenHandler(BaseHandler):

    async def post(self):
        cache = RefreshTokenCache()
        user = self.data.get('_user')
        remaining_time = user.remaining_time
        # 限制前端频繁的刷新token
        if remaining_time > settings.REFRESH_TOKEN_MAX_TIME:
            raise CustomizeError('不能重复刷新token')
        refresh_token = self.data.get('refresh_token')
        if not refresh_token:
            raise ParamsError('参数缺失')
        # check refresh_token
        old_refresh_token = await cache.get_refresh_token_by_phone(user.phone)
        if not old_refresh_token == refresh_token:
            raise CustomizeError(msg='refresh_token已经过期，请重新登录')
        # generate new token
        new_token = merchant_to_token(user)
        new_refresh_token = uuid.uuid1().hex
        # flush refresh_token
        try:
            await cache.set_refresh_token_by_phone(user.phone, refresh_token, timeout=settings.REFRESH_TOKEN_EXPIRATION)
        except Exception as e:
            get_logger().error(f"功能：RefreshToken || 状态：失败 || 失败信息:{e}")
        self.response_data(info={
            'access_token': new_token,
            'refresh_token': new_refresh_token
        })


# 修改密码
class ModifyPasswordHandler(BaseHandler):
    ...


# 修改个人信息
class ModifyMyselfInfoHandler(BaseHandler):
    ...


# 忘记密码
class ForgetPasHandler(BaseHandler):
    ...


# 退出登录
class LogoutHandler(BaseHandler):

    def post(self):
        ...


# __*__coding:utf-8__*__
# @ModuleName: 获取验证码、用户注册功能
# @Function: CodeHandler、RegisterHandler
# @Author: pl
# @Time: 2021/11/4 9:52
import threading
import time
from datetime import datetime

from cache.cache_code import CodeCache
from common.exceptions import OSInnerError, ParamsError, CustomizeError, MySQLError
from conf import settings
from dao.merchant_dao import MerchantDao
from handlers.base_handler import BaseHandler
from models.users import Merchant
from tasks import tasks_set
from utils.utils import gen_sms_code, make_password, distribute_avatar
from utils.web_log import get_logger
from validation import BaseValidation, NotEmpty, IsPhone, IsNum, NotNull, Min


class CodeHandler(BaseHandler):

    async def post(self):
        cache = CodeCache()
        validated_data = BaseValidation.valid_data(
            self.data,
            {
                'phone': [NotEmpty(), IsPhone()],
            }
        )
        phone = validated_data.validated_data.get('phone')
        if await MerchantDao.get_merchant_exists_by_phone(phone=phone):
            raise CustomizeError(msg="该手机号码已经注册，请更换号码后继续")

        if await cache.get_code_request_expiration(phone):
            raise CustomizeError(msg="请求过于频繁,请稍后再试")

        # 生成短信验证码
        sms_code = gen_sms_code()
        try:
            await cache.set_code(phone, sms_code, settings.CODE_EXPIRATION)
            await cache.set_code_request_expiration(phone, 1, settings.CODE_REQUEST_EXPIRATION)
        except Exception as e:
            get_logger().info(f"功能：获取短信验证码 || 状态：失败 || 请求手机号；{phone} || 短信验证码： {sms_code} || 失败原因：{str(e)}")
            raise OSInnerError('系统内部服务异常,请联系管理员')
        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 发短信任务塞到任务队列
        await tasks_set.send_sms_code(phone, sms_code)
        # 记录日志
        get_logger().info(f"功能：获取短信验证码 || 状态：成功 || 请求手机号；{phone} || 短信验证码： {sms_code} || 任务入列时间：{send_time}")
        return self.response_data(msg='短信发送成功，请注意查收')


# 注册
class RegisterHandler(BaseHandler):

    async def post(self):
        cache = CodeCache()
        validated_data = BaseValidation.valid_data(
            self.data,
            {
                'phone': [NotEmpty(), IsPhone()],
                'password': [NotEmpty(), Min(8)],
                'code': [NotEmpty(), IsNum()],
                'company': [NotNull()],
                'postbox': [NotNull()]
            }
        )
        phone = validated_data.validated_data.get('phone')
        # 再做一次用户注册检测（防止发送多次验证码造成多次点击注册按钮，造成入库错误）
        if await MerchantDao.get_merchant_exists_by_phone(phone=phone):
            raise CustomizeError(msg="该手机号码已经注册，请更换号码后继续")
        # 校验验证码(多次请求短信验证码会覆盖)
        local_code = await cache.get_code(phone)
        if not validated_data.validated_data.get('code') == local_code:
            raise ParamsError(msg='短信验证码验证失败')
        # 处理密码
        validated_data.validated_data['password'] = make_password(validated_data.validated_data.get('password'))
        # 默认数据封装进validated_data
        validated_data['avatar'] = distribute_avatar()
        validated_data['grade'] = 1  # 默认通过注册获得的账号是一级用户（其他的通过一级用户创建的用户都是二级用户）
        try:
            await MerchantDao.create_merchant(Merchant.clean_data(validated_data.validated_data))
        except Exception as e:
            get_logger().error(f'功能：用户注册功能 || 状态：失败 || 失败原因：{str(e)}')
            raise MySQLError()
        # 注册成功，删除缓存（防止多次注册）
        await cache.delete_code(phone)
        await cache.delete_code_request_expiration(phone)
        # 记录日志
        get_logger().info(f"功能：用户注册功能 || 状态：成功 || 手机号：{ phone }")
        return self.response_data(msg='用户注册成功，请返回登录')
# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/23 14:29
import json
from django.conf import settings
# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import CommonRequest


async def sms(mobile, code, template_code):
    """
    阿里云发送短信验证码工具
    :param mobile: 手机号
    :param code: 验证码
    :param template_code: 模板编号
    :return:
    """
    ...
    # try:
    #     client = AcsClient(settings.PUBLIC_KEY_ID, settings.PRIVATE_KEY)
    #     request = CommonRequest()
    #     request.set_accept_format('json')
    #     request.set_domain('dysmsapi.aliyuncs.com')
    #     request.set_method('POST')
    #     request.set_protocol_type('https')  # https | http
    #     request.set_version('2017-05-25')
    #     request.set_action_name('SendSms')
    #     request.add_query_param('SignName', settings.SIGN_NAME)
    #     request.add_query_param('PhoneNumbers', mobile)
    #     request.add_query_param('TemplateCode', template_code)
    #     request.add_query_param('TemplateParam', {"code": code})
    #     response = client.do_action_with_exception(request)
    #     res_dict = json.loads(response)
    # except Exception as e:
    #     res_dict = {'Code': 'No'}
    #     return res_dict
    # else:
    #     return res_dict
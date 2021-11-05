# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/4 9:52
from dao.users_dao import UsersDao
from handlers.base_handler import BaseHandler
from utils.utils import gen_sms_code
from validation import BaseValidation, NotEmpty, IsPhone, IsNum, NotNull

"""
涉及功能：
注册
忘记密码
登录
"""


# 注册
class RegisterHandler(BaseHandler):

    def post(self):
        """
        手机号：phone
        验证码：code
        登录密码：做aes对称加密
        企业名称：
        时间戳：
        加密：
        :return:
        """
        BaseValidation.valid_data(
            self.data,
            {
                'phone': [NotEmpty(), IsPhone()],
            }
        )
        if UsersDao.get_merchant_by_phone(**self.data):
            self.response_data("该手机号码已经注册，请更换号码后继续")
        # 注册验证码
        # code = gen_sms_code()

        BaseValidation.valid_data(
            self.data,
            {
                'phone': [NotEmpty(), IsPhone()],
                'password': [NotEmpty()],
                'code': [NotEmpty(), IsNum()],
                'company': [NotNull()],
                'postbox': [NotNull()]
            }
        )

        # result = UsersDao.add_merchant(**self.data)


        self.response_data({
            'result': 'ok'
        })


# 登录
class LoginHandler(BaseHandler):

    def post(self):
        data = self.data


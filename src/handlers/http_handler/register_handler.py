# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/4 9:52
from handlers.base_handler import BaseHandler
from controller.users_controller import UsersController
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
                'password': [NotEmpty()],
                'code': [NotEmpty(), IsNum()],
                'company': [NotNull()],
                'postbox': [NotNull()]
            }
        )
        result = UsersController().merchant_register(**self.data)
        self.response_data(result)


# 登录
class LoginHandler(BaseHandler):

    def post(self):
        data = self.data


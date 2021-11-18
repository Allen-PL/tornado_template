# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/4 9:52
from connector.mysql_connector import sync_session
from dao.users_dao import UsersDao
from handlers.base_handler import BaseHandler
from models.users import Merchant
from utils.utils import gen_sms_code
from utils.web_log import get_logger
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
        # if UsersDao.get_merchant_by_phone(**self.data):
        #     return self.response_data("该手机号码已经注册，请更换号码后继续")
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

        """（所以就有两种序列化的方案：单张表的基于对象序列化；单张表或者多张表的基于字典的再序列化）
        涉及多张表的时候怎么处理(全部字段组合成dict再处理)
        字段显示部分怎么处理（通过exclude/fields两个方法来实现）
        字段不以源数据格式展示怎么办（可以加多个方法的来实现，比如int_to_str("字段名称")）
        """
        instances = Merchant().get_list(self.data)
        Merchant().serializer(instances)


        return self.response_data({
            'result': 'ok'
        })



# 登录
class LoginHandler(BaseHandler):

    def post(self):
        data = self.data


"""
错误信息在控制台打印三遍，解决这个问题
"""

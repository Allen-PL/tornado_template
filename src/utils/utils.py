# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/5 14:22


# generate sms code
import random


def gen_sms_code() -> str:
    code = ''
    while len(code) < 6:
        code += str(random.randint(0, 9))
    return code


if __name__ == '__main__':
    print(gen_sms_code())
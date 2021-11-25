# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/5 14:22
import random
import hashlib

from conf import settings


# generate sms code
def gen_sms_code() -> str:
    code = ''
    while len(code) < 6:
        code += str(random.randint(0, 9))
    return code


# encryption of sha1
def make_password(plaintext: str) -> str:
    sha1 = hashlib.sha1(settings.COMMON_SALT.encode('utf-8'))
    sha1.update(plaintext.encode('utf-8'))
    return sha1.hexdigest()


# decryption of sha1
def check_password(plaintext: str, ciphertext: str) -> bool:
    return make_password(plaintext) == ciphertext


# distribute users the default avatar
def distribute_avatar():
    return random.choice(settings.USERS_DEFAULT_AVATAR)


if __name__ == '__main__':
    # print(gen_sms_code())
    # print(make_password('pl'))
    # print(check_password('pl', 'dc8d06050dcd268ea428097c97f4cef074160b1'))
    print(distribute_avatar())
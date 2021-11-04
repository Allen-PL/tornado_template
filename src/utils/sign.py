# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/4 10:31
import hashlib
from conf import settings


# generate sign
from common.exceptions import SignatureError, ParamsError


def gen_str_from_data(data: dict):
    r_list = []
    for k in sorted(data):
        if type(data.get(k)) != str:
            if type(data.get(k)) == bool:
                stringA: str = "{0}={1}".format(k, str(data.get(k)).lower())
            else:
                stringA = "{0}={1}".format(k, data.get(k))
            stringA = stringA.replace("'", '"')
            stringA = stringA.replace(" ", "")
        else:
            stringA = "{0}={1}".format(k, data.get(k))
        r_list.append(stringA)
    return "&".join(r_list)


# check sign
def check_sign(data: dict):
    try:
        if settings.DEBUG:
            return True
    except Exception:
        pass
    if 'sign' not in data.keys() or 'time' not in data.keys():
        raise ParamsError(msg='缺少必须参数，请检查之后再上传')
    origin_sign = str(data.pop('sign'))
    origin_time = str(data.get('time'))
    if len(origin_time) != 13:
        raise ParamsError(msg='time参数请传入13位的时间戳')
    # 对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = gen_str_from_data(data)
    # print(stringA, '==================1')
    obj = hashlib.md5(origin_time.encode())  # 实例化md5的时候可以给传个参数，这叫加盐
    obj.update(stringA.encode("utf-8"))
    sign = obj.hexdigest()
    # print(sign, '====================2')
    if not sign == origin_sign:
        raise SignatureError()


if __name__ == '__main__':

    data = {
        'username': '15839996222',
        'password': '123456',
        'store_no': 'CXCS',
        'time': '1621836731798',
        'sign': 'adgfndfsg'
    }
    res = check_sign(data=data)
    print(res)

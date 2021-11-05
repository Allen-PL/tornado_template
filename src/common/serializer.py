# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/5 14:29
from typing import List

from models.base import Base
from models.users import Merchant


class DynamicFieldsSerializer:
    """动态的选择需要序列化的字段"""

    def __init__(self, data: List, **kwargs):
        self.data: List = data
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        if fields and exclude_fields:
            raise ValueError('fields 和 exclude_fields 不能同时存在')
        if fields is not None:
            allowed = set(fields)
            existing = set(data[0].keys())
            for field_name in existing - allowed:
                for dct in self.data:
                    dct.pop(field_name)
        if exclude_fields is not None:
            disallowed = set(exclude_fields)
            for field_name in disallowed:
                for dct in self.data:
                    dct.pop(field_name, None)


if __name__ == '__main__':
    data = [
        {
            "name": "pl",
            "age": 18
        },
        {
            "name": "pl1",
            "age": 20,
            "sex": "sales"
        },
    ]
    data = DynamicFieldsSerializer(data, fields=['name', 'age', 'xx'])

    print(data.data)
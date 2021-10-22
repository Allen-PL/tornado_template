""" 
@Function:
@Author  : ybb
@Time    : 2020/9/28 18:12
"""
from .exceptions import ValidException, FieldValidException
from .field_validation import FieldValidation


class BaseValidation(object):
    """用户创建需要校验的字段"""

    def __init__(self, data):
        self._valid(data)
        self._data = data

    def _valid(self, data):
        errors = {}
        validated_data = {}
        for field, rules in self.valid_rules().items():
            val = data.get(field)
            field_errors = []
            ret_val = None
            for rule in rules:  # type: FieldValidation
                try:
                    ret_val = rule.valid(val)
                except FieldValidException as e:
                    field_errors.append(e.msg)
            if not field_errors:
                validated_data[field] = ret_val
                continue
            errors[field] = field_errors
        if errors:
            raise ValidException(info=errors, msg='数据校验错误')
        self.validated_data = validated_data

    def valid_rules(self):
        """校验规则, 返回字典, [列表是一个校验器]
        return {
            'username': [NotNull(message=""), Min(2)],
            'password': [],
            'phone': [],
            'display': [],
        }
        """
        raise ValueError('必须定义校验规则')

    @classmethod
    def valid_data(cls, data, rules) -> 'BaseValidation':
        """
        :param {dict} data:
        :param {dict} rules:
        :return: {BaseValidation}
        """
        return type('__Validation', (cls,), {'valid_rules': lambda self: rules})(data)

    def __str__(self):
        """打印所有的_data信息"""
        return str(self._data)

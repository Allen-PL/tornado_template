# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/28 15:25
from enum import Enum, unique


@unique
class EnumUserStatus(Enum):

    # default user is activited.
    DEFAULT = 1

    @property
    def status(self):
        return self.status


@unique
class EnumUserGroup(Enum):

    pass


@unique
class EnumUserMark(Enum):

    OTHER = 0
    INTERNAL_USER = 1
    EXTERNAL_USER = 2

    @property
    def mark(self):
        return {
            'OTHER': self.OTHER,
            'INTERNAL_USER': self.INTERNAL_USER,
            'EXTERNAL_USER': self.EXTERNAL_USER
        }


@unique
class EnumRoleType(Enum):
    INTERNAL_ROLE = 1
    EXTERNAL_ROLE = 2

    @property
    def type(self):
        return {
            'INTERNAL_ROLE': self.INTERNAL_ROLE,
            'EXTERNAL_ROLE': self.EXTERNAL_ROLE
        }


@unique
class EnumSection(Enum):
    H_SECTION = 1
    V_SECTION = 2

    @property
    def type_choices(self):
        return (
            (EnumSection.H_SECTION, '横断面'),
            (EnumSection.V_SECTION, '纵断面')
        )


@unique
class EnumLog(Enum):
    ADD_OPERATING = 1
    UPDATE_OPERATING = 2
    DELETE_OPERATING = 3
    OTHER_OPERATING = 4

    @property
    def type_log(cls):
        return (
            (cls.ADD_OPERATING, '添加操作'),
            (cls.UPDATE_OPERATING, '编辑操作'),
            (cls.DELETE_OPERATING, '删除操作'),
            (cls.OTHER_OPERATING, '其他操作'),
        )
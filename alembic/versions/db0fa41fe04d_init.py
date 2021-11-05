"""init

Revision ID: db0fa41fe04d
Revises: b6f12253eb7d
Create Date: 2021-10-28 17:28:54.238007

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'db0fa41fe04d'
down_revision = 'b6f12253eb7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'create_time',
               existing_type=mysql.DATETIME(),
               comment='创建时间',
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('user', 'update_time',
               existing_type=mysql.DATETIME(),
               comment='更新时间',
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('user', 'id',
               existing_type=mysql.INTEGER(),
               comment='ID',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('user', 'nickname',
               existing_type=mysql.VARCHAR(length=32),
               comment='昵称(用于登录)',
               existing_nullable=False)
    op.alter_column('user', 'realname',
               existing_type=mysql.VARCHAR(length=32),
               comment='真实姓名',
               existing_nullable=False)
    op.alter_column('user', 'phone',
               existing_type=mysql.VARCHAR(length=18),
               comment='手机号(用于登录)',
               existing_nullable=False)
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=128),
               comment='用于密码',
               existing_nullable=False)
    op.alter_column('user', 'avatar',
               existing_type=mysql.VARCHAR(length=256),
               comment='用户头像',
               existing_nullable=False)
    op.alter_column('user', 'state',
               existing_type=mysql.TINYINT(display_width=1),
               comment='账户状态',
               existing_nullable=True)
    op.alter_column('user', 'group',
               existing_type=mysql.BIGINT(),
               comment='用户组',
               existing_nullable=False)
    op.alter_column('user', 'extra_field1',
               existing_type=mysql.VARCHAR(length=256),
               comment='冗余字段1',
               existing_nullable=True)
    op.alter_column('user', 'extra_field2',
               existing_type=mysql.VARCHAR(length=256),
               comment='冗余字段2',
               existing_nullable=True)
    op.alter_column('user', 'extra_field3',
               existing_type=mysql.VARCHAR(length=256),
               comment='冗余字段3',
               existing_nullable=True)
    op.alter_column('user', 'extra_field4',
               existing_type=mysql.VARCHAR(length=256),
               comment='冗余字段4',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'extra_field4',
               existing_type=mysql.VARCHAR(length=256),
               comment=None,
               existing_comment='冗余字段4',
               existing_nullable=True)
    op.alter_column('user', 'extra_field3',
               existing_type=mysql.VARCHAR(length=256),
               comment=None,
               existing_comment='冗余字段3',
               existing_nullable=True)
    op.alter_column('user', 'extra_field2',
               existing_type=mysql.VARCHAR(length=256),
               comment=None,
               existing_comment='冗余字段2',
               existing_nullable=True)
    op.alter_column('user', 'extra_field1',
               existing_type=mysql.VARCHAR(length=256),
               comment=None,
               existing_comment='冗余字段1',
               existing_nullable=True)
    op.alter_column('user', 'group',
               existing_type=mysql.BIGINT(),
               comment=None,
               existing_comment='用户组',
               existing_nullable=False)
    op.alter_column('user', 'state',
               existing_type=mysql.TINYINT(display_width=1),
               comment=None,
               existing_comment='账户状态',
               existing_nullable=True)
    op.alter_column('user', 'avatar',
               existing_type=mysql.VARCHAR(length=256),
               comment=None,
               existing_comment='用户头像',
               existing_nullable=False)
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=128),
               comment=None,
               existing_comment='用于密码',
               existing_nullable=False)
    op.alter_column('user', 'phone',
               existing_type=mysql.VARCHAR(length=18),
               comment=None,
               existing_comment='手机号(用于登录)',
               existing_nullable=False)
    op.alter_column('user', 'realname',
               existing_type=mysql.VARCHAR(length=32),
               comment=None,
               existing_comment='真实姓名',
               existing_nullable=False)
    op.alter_column('user', 'nickname',
               existing_type=mysql.VARCHAR(length=32),
               comment=None,
               existing_comment='昵称(用于登录)',
               existing_nullable=False)
    op.alter_column('user', 'id',
               existing_type=mysql.INTEGER(),
               comment=None,
               existing_comment='ID',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('user', 'update_time',
               existing_type=mysql.DATETIME(),
               comment=None,
               existing_comment='更新时间',
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('user', 'create_time',
               existing_type=mysql.DATETIME(),
               comment=None,
               existing_comment='创建时间',
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    # ### end Alembic commands ###
"""init

Revision ID: a317dd1ded6c
Revises: 
Create Date: 2021-11-22 14:48:43.094758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a317dd1ded6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('username', sa.String(length=32), nullable=True, comment='用户姓名'),
    sa.Column('phone', sa.String(length=18), nullable=False, comment='手机号(用于登录)'),
    sa.Column('password', sa.String(length=128), nullable=False, comment='密码'),
    sa.Column('avatar', sa.String(length=256), nullable=False, comment='管理员头像'),
    sa.Column('status', sa.Boolean(), nullable=True, comment='账户状态'),
    sa.Column('no', sa.String(length=32), nullable=False, comment='工号'),
    sa.Column('department', sa.String(length=64), nullable=True, comment='部门'),
    sa.Column('last_time', sa.DateTime(), nullable=True, comment='最后登录时间'),
    sa.Column('ipaddr', sa.String(length=32), nullable=True, comment='登录ip地址'),
    sa.Column('postbox', sa.String(length=64), nullable=True, comment='邮箱'),
    sa.Column('superuser', sa.Boolean(), nullable=True, comment='标记超级管理员'),
    sa.Column('extra_field1', sa.String(length=256), nullable=True, comment='冗余字段1'),
    sa.Column('extra_field2', sa.String(length=256), nullable=True, comment='冗余字段2'),
    sa.Column('extra_field3', sa.String(length=256), nullable=True, comment='冗余字段3'),
    sa.Column('extra_field4', sa.String(length=256), nullable=True, comment='冗余字段4'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_admin_department'), 'admin', ['department'], unique=False)
    op.create_index(op.f('ix_admin_phone'), 'admin', ['phone'], unique=True)
    op.create_table('arole',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('r_name', sa.String(length=32), nullable=False, comment='角色名称'),
    sa.Column('r_code', sa.String(length=32), nullable=False, comment='角色代码'),
    sa.Column('r_desc', sa.String(length=256), nullable=True, comment='角色描述'),
    sa.Column('r_status', sa.Boolean(), nullable=True, comment='角色状态'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('r_code'),
    sa.UniqueConstraint('r_name')
    )
    op.create_table('merchant',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('phone', sa.String(length=18), nullable=False, comment='手机号(用于登录)'),
    sa.Column('password', sa.String(length=128), nullable=False, comment='用于密码'),
    sa.Column('avatar', sa.String(length=256), nullable=True, comment='用户头像'),
    sa.Column('status', sa.Boolean(), nullable=True, comment='账户状态'),
    sa.Column('no', sa.String(length=32), nullable=True, comment='工号'),
    sa.Column('department', sa.String(length=64), nullable=True, comment='部门'),
    sa.Column('last_time', sa.DateTime(), nullable=True, comment='最后登录时间'),
    sa.Column('ipaddr', sa.String(length=32), nullable=True, comment='登录ip地址'),
    sa.Column('company', sa.String(length=32), nullable=True, comment='所属公司'),
    sa.Column('postbox', sa.String(length=64), nullable=True, comment='邮箱'),
    sa.Column('grade', sa.Integer(), nullable=False, comment='用户级别（注册用户默认0，平台添加用户的为1）'),
    sa.Column('extra_field1', sa.String(length=256), nullable=True, comment='冗余字段1'),
    sa.Column('extra_field2', sa.String(length=256), nullable=True, comment='冗余字段2'),
    sa.Column('extra_field3', sa.String(length=256), nullable=True, comment='冗余字段3'),
    sa.Column('extra_field4', sa.String(length=256), nullable=True, comment='冗余字段4'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_merchant_department'), 'merchant', ['department'], unique=False)
    op.create_index(op.f('ix_merchant_phone'), 'merchant', ['phone'], unique=True)
    op.create_table('mrole',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('r_name', sa.String(length=32), nullable=False, comment='角色名称'),
    sa.Column('r_code', sa.String(length=32), nullable=False, comment='角色代码'),
    sa.Column('r_desc', sa.String(length=256), nullable=True, comment='角色描述'),
    sa.Column('r_status', sa.Boolean(), nullable=True, comment='角色状态'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('r_code'),
    sa.UniqueConstraint('r_name')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('p_name', sa.String(length=32), nullable=False, comment='权限名称'),
    sa.Column('P_code', sa.String(length=32), nullable=False, comment='权限代码'),
    sa.Column('uri', sa.String(length=128), nullable=False, comment='权限对应的uri'),
    sa.Column('method', sa.String(length=12), nullable=False, comment='uri对应的方法'),
    sa.Column('p_desc', sa.String(length=256), server_default='', nullable=True, comment='权限描述'),
    sa.Column('p_status', sa.Boolean(), nullable=True, comment='权限状态'),
    sa.Column('p_type', sa.Boolean(), nullable=False, comment='权限类型（标记内部人员独有的权限）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('P_code'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('p_name'),
    sa.UniqueConstraint('uri', 'method', name='ix_uri_method')
    )
    op.create_table('pk_admin_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('u_id', sa.BigInteger(), nullable=False, comment='管理员id'),
    sa.Column('r_id', sa.BigInteger(), nullable=False, comment='角色id'),
    sa.Column('status', sa.Boolean(), nullable=True, comment='用户角色关联状态'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_pk_admin_role_r_id'), 'pk_admin_role', ['r_id'], unique=False)
    op.create_index(op.f('ix_pk_admin_role_u_id'), 'pk_admin_role', ['u_id'], unique=False)
    op.create_table('pk_admin_role_permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('r_id', sa.BigInteger(), nullable=False, comment='管理员角色id'),
    sa.Column('p_id', sa.BigInteger(), nullable=False, comment='权限id'),
    sa.Column('status', sa.Boolean(), nullable=True, comment='角色权限关联状态'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_pk_admin_role_permission_p_id'), 'pk_admin_role_permission', ['p_id'], unique=False)
    op.create_index(op.f('ix_pk_admin_role_permission_r_id'), 'pk_admin_role_permission', ['r_id'], unique=False)
    op.create_table('pk_merchant_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('u_id', sa.BigInteger(), nullable=False, comment='商户id'),
    sa.Column('r_id', sa.BigInteger(), nullable=False, comment='角色id'),
    sa.Column('status', sa.Boolean(), nullable=True, comment='用户角色关联状态'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_pk_merchant_role_r_id'), 'pk_merchant_role', ['r_id'], unique=False)
    op.create_index(op.f('ix_pk_merchant_role_u_id'), 'pk_merchant_role', ['u_id'], unique=False)
    op.create_table('pk_merchant_role_permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.Column('r_id', sa.BigInteger(), nullable=False, comment='商户角色id'),
    sa.Column('p_id', sa.BigInteger(), nullable=False, comment='权限id'),
    sa.Column('status', sa.Boolean(), nullable=True, comment='角色权限关联状态'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_pk_merchant_role_permission_p_id'), 'pk_merchant_role_permission', ['p_id'], unique=False)
    op.create_index(op.f('ix_pk_merchant_role_permission_r_id'), 'pk_merchant_role_permission', ['r_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pk_merchant_role_permission_r_id'), table_name='pk_merchant_role_permission')
    op.drop_index(op.f('ix_pk_merchant_role_permission_p_id'), table_name='pk_merchant_role_permission')
    op.drop_table('pk_merchant_role_permission')
    op.drop_index(op.f('ix_pk_merchant_role_u_id'), table_name='pk_merchant_role')
    op.drop_index(op.f('ix_pk_merchant_role_r_id'), table_name='pk_merchant_role')
    op.drop_table('pk_merchant_role')
    op.drop_index(op.f('ix_pk_admin_role_permission_r_id'), table_name='pk_admin_role_permission')
    op.drop_index(op.f('ix_pk_admin_role_permission_p_id'), table_name='pk_admin_role_permission')
    op.drop_table('pk_admin_role_permission')
    op.drop_index(op.f('ix_pk_admin_role_u_id'), table_name='pk_admin_role')
    op.drop_index(op.f('ix_pk_admin_role_r_id'), table_name='pk_admin_role')
    op.drop_table('pk_admin_role')
    op.drop_table('permission')
    op.drop_table('mrole')
    op.drop_index(op.f('ix_merchant_phone'), table_name='merchant')
    op.drop_index(op.f('ix_merchant_department'), table_name='merchant')
    op.drop_table('merchant')
    op.drop_table('arole')
    op.drop_index(op.f('ix_admin_phone'), table_name='admin')
    op.drop_index(op.f('ix_admin_department'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
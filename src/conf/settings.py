# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/10/13 16:46
import os
if os.environ.get('prod') == 'prod':
    from .prod import *
else:
    from .dev import *

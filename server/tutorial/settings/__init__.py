import os
"""
export django_ENV= prod  也可以添加docker 一般默认开发环境
"""

if os.getenv('django_ENV') == 'prod':
    from .prod import *
else:
    from .dev import *





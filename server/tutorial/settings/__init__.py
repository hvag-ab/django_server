import os
import platform
"""
export django_ENV= prod  也可以添加docker 一般默认开发环境
"""

system = platform.system().lower() != 'linux'

if os.getenv('DJANGO_ENV') == 'dev' or system:
    from .prod import *
else:
    from .dev import *





# 在 mac 和 windows 电脑上为开发环境，生产环境一般为 linux
from util.host import host_os

if host_os == 'linux':
    from .prod import *
else:
    from .dev import *

# from .docker import *



import os
from django.utils import timezone
from django.conf import settings
from celery import Celery
from celery import platforms

from . import celeryconfig # 导入celery配置文件

# 为celery设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"tutorial.settings")
print(f"{settings.PROJECT_NAME}.settings")
## 创建celery app
app = Celery('celery_tasks')

# 从单独的配置模块中加载配置
app.config_from_object(celeryconfig)

# 设置app自动加载任务 celery_tasks模块下的tasks 和 每个app模块下的tasks
app.autodiscover_tasks(['celery_tasks'])

# 解决时区问题,定时任务启动就循环输出
# app.now = timezone.now
# 强制以root用户运行 django 运行用户实际为非root用户
platforms.C_FORCE_ROOT = True




"""
celery并发计算规则
celery任务并发只与celery配置项CELERYD_CONCURRENCY 有关，与CELERYD_MAX_TASKS_PER_CHILD没有关系，即CELERYD_CONCURRENCY=2，只能并发2个worker，
此时任务处理较大的文件时，执行两次可以看到两个task任务并行执行，而执行第三个任务时，开始排队，直到两个worker执行完毕。

worker和beat的停止

ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9
ps auxww | awk '/celery beat/ {print $2}' | xargs kill -9

4. 分布式集群部署
celery作为分布式的任务队列框架，worker是可以执行在不同的服务器上的。部署过程和单机上启动是一样。
只要把项目代码copy到其他服务器，使用相同命令就可以了。可以思考下，这个是怎么实现的？对了，就是通过共享Broker队列。
使用合适的队列，如redis，单进程单线程的方式可以有效的避免同个任务被不同worker同时执行的情况。

cd django项目中的manage.py同一层级文件里
celery -A celery_tasks worker -l debug

windows系统启动:

pip install gevent
celery -A celery_tasks worker -l info -P gevent

celery beat 启动
INSTALLED_APPS = [
    # ...
    #'django_celery_results',  # 查看 celery 执行结果
    'django_celery_beat',  # pip install django-celery-beat
]
$ python manage.py migrate
celery -A celery_tasks beat --loglevel INFO
# windows下
celery -A celery_tasks beat -l info -P gevent

"""
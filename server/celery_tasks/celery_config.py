import os
from django.conf import settings
from kombu import Exchange, Queue
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.dev")

REDIS = settings.REDIS

# 设置代理人broker
broker_url =  f"{REDIS}/7"

# 设置默认不存结果
IGNORE_RESULT = False
# 指定 结果Backend
# result_backend = f"{REDIS}/8" # redis后端
result_backend = 'django-db' # 设置执行结果保存到django的数据库中 是结果生成后才保存所以不能在tasks运行中使用。
"""
$ pip install django-celery-results
INSTALLED_APPS = [
'django_celery_results',
]
$ python manage.py migrate  
"""
# BROKER_POOL_LIMIT = 50
# REDIS_MAX_CONNECTIONS = 60
# BROKER_TRANSPORT_OPTIONS = {
#     "max_connections": 400,
# }
#

# 设置每个app模块的文件名 默认tasks
# CELERY_IMPORTS = ('tasks',)

# celery 序列化与反序列化配置
TASK_SERIALIZER = 'pickle'
RESULT_SERIALIZER = 'pickle'
ACCEPT_CONTENT = ['pickle', 'json']

# 可选参数：给某个任务限流
# task_annotations = {'celery_task.tasks.xx': {'rate_limit': '10/s'}}

# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。 设为0，存储结果永不过期
TASK_RESULT_EXPIRES = 10

# celery 的启动工作数量设置
WORKER_CONCURRENCY = 10

# 有些情况可以防止死锁
FORCE_EXECV = True

# 任务预取功能，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
PREFETCH_MULTIPLIER = 20

# 设置并发的worker数量
CONCURRENCY = 4

# celery 的 worker 执行多少个任务后进行重启操作
WORKER_MAX_TASKS_PER_CHILD = 100

# 任务发送完成是否需要确认，这一项对性能有一点影响
ACKS_LATE = False

# 每个worker执行了多少任务就会销毁，防止内存泄露，默认是无限的
MAX_TASKS_PER_CHILD = 4

# 禁用所有速度限制，如果网络资源有限，不建议开足马力。
DISABLE_RATE_LIMITS = True

# 规定完成任务的时间
TASK_TIME_LIMIT = 15 * 60  # 在15分钟内完成任务，否则执行该任务的worker将被杀死，任务移交给父进程

TIMEZONE = settings.TIME_ZONE
# 是否启用UTC时间  默认为True
ENABLE_UTC = False

# 队列设置
"""
一个broker上面开辟多个队列，每个队列绑定指定类型的任务，而对应的worker通过指定的队列获取任务
其中需要交换机exchange 和 queue 

from kombu import Exchange, Queue

exchange 交换机说明  交换机type有三个类型 
type= “direct”  redis只支持这个类型 其他类型是rabbitmq才能支持
direct类型的Exchange路由规则也很简单，它会把消息路由到那些binding key与routing_key完全匹配的Queue中。
例子：
CELERY_QUEUES = (
    Queue('for_adds',Exchange('for_adds',type='direct'), routing_key='adds'),
    Queue('for_send_emails', Exchange('for_adds',type='direct'), routing_key='email'),
)
CELERY_ROUTES = {
    'celery_test.tasks.add': {'exchange':'for_adds','routing_key':'add'},
    'celery_test.tasks.send_mail': {'exchange':'for_adds','routing_key':'email'},
}
result = mul.apply_async(args=(2, 2), queue='task_heavy', routing_key='', exchange='')

type= “topic”
topic类型的Exchange在匹配规则上进行了扩展，它与direct类型的Exchage相似，也是将消息路由到
binding key与routing key相匹配的Queue中。可以看出和上面那个区别的地方，这里面不
是强匹配。它引入了两个通配符#和*前者匹配多个单词（可以为0），后者匹配一个单词。
CELERY_QUEUES = (
    Queue('for_adds',Exchange('for_adds',type='topic'), routing_key='*.task.*'),
    Queue('for_send_emails', Exchange('for_adds',type='topic'), routing_key='*.*.email'),
    Queue('add', Exchange('for_adds',type='topic'), routing_key='*.add'),
)
CELERY_ROUTES = {
    'celery_test.tasks.add': {'exchange':'for_adds','routing_key':'q.task.email'},
    'celery_test.tasks.send_mail': {'exchange':'for_adds','routing_key':'a.task.e'},
    'celery_test.tasks.adds': {'exchange':'for_adds','routing_key':'b.add'},
}

type = "fanout"
fanout类型就是传说中的广播形式，它没有参数绑定，就是不需要指定上面的routing_key之类的东西，
只要和该交换绑定的queue，统统发送出去。类似于通过交换口，就广播发出。
CELERY_QUEUES = (
    Queue('for_adds',Exchange('for_adds',type='fanout')),
    Queue('for_send_emails', Exchange('for_adds',type='fanout')),
    Queue('add', Exchange('for_adds',type='fanout')),
)
CELERY_ROUTES = {
    'celery_test.tasks.add': {'exchange':'for_adds'},
    'celery_test.tasks.send_mail': {'exchange':'for_adds',},
    'celery_test.tasks.adds': {'exchange':'for_adds',},
}

在设想你有某个任务，相当耗费时间，但是却要求很高的实时性,那么你可以需要多台服务器的多个workers一起工作，每个服务器负担其中的一部分,但是celerybeat只会生成一个任务,被某个worker取走就没了,
所以你需要让每个服务器的队列都要收到这个消息.这里很需要注意的是:你的fanout类型的消息在生成的时候为多份,每个队列一份，而不是一个消息发送给单一队列的次数

"""

# 设置默认的队列名称，如果一个消息不符合其他的队列就会放在默认队列里面，如果什么都不设置的话，
# 数据都会发送到默认的队列中
DEFAULT_QUEUE = "default"

# 设置详细的队列 （如果不设置队列 那么就用默认队列）
QUEUES = (
    Queue('default', exchange=Exchange('default', type="direct"), routing_key='default'),
    Queue('task_light', exchange=Exchange('task_light'), routing_key='task_light'),
    Queue('task_heavy', exchange=Exchange('task_heavy'), routing_key='task_heavy'),
)

"""
任务指定特定的worker执行

启动worker时，-Q 指定worker支持的任务列队名, 可以支持多个队列名哦

celery -A celery_tasks.celery_main worker -l debug -c 4 -Q default,task_heavy
任务调用时， queue=*来指定需要执行worker
也可以下面这种设置
显然是并发的。-c参数定义工作者创建的并发线程数。

(venv) $ celery -A celery_tasks.celery_main worker -l info -Q default -c 2
(venv) $ celery -A celery_tasks.celery_main worker -l info -Q low_priority -c 1
(venv) $ celery -A celery_tasks.celery_main worker -l info -Q high_priority -c 4
并具有自动缩放工人

(venv) $ celery -A celery_tasks.celery_main worker -l info -Q default --autoscale 4,2
(venv) $ celery -A celery_tasks.celery_main worker -l info -Q low_priority --autoscale 2,1
(venv) $ celery -A celery_tasks.celery_main worker -l info -Q high_priority --autoscale 8,4
这样，您可以控制任务的消耗速度。

并发数应保持接近CPU核心数。如果服务器具有4个核心CPU，则最大并发数应为4。当然，更大的数字将起作用，但效率较低。


"""


# 定时任务
# celery beat配置（周期性任务设置）
# ENABLE_UTC = False
# DJANGO_CELERY_BEAT_TZ_AWARE = False
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# # 初始化定时任务
# from celery.schedulers import crontab
# # CELERY_BEAT_SCHEDULE = {
# #     "sample_task": {
# #         "task": "core.tasks.sample_task",
# #         "schedule": crontab(minute="*/1"),
# #     },
# # }

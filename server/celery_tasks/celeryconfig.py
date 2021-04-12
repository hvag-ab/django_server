import os
from django.conf import settings
# from celery.schedulers import crontab
from kombu import Exchange, Queue
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"tutorial.settings")

REDIS = settings.REDIS
print('redisbackend',REDIS)

# 设置代理人broker
broker_url =  f"{REDIS}/7"
# 指定 结果Backend
result_backend = f"{REDIS}/8"
# BROKER_POOL_LIMIT = 50
# CELERY_REDIS_MAX_CONNECTIONS = 60
# BROKER_TRANSPORT_OPTIONS = {
#     "max_connections": 400,
# }
#
# 指定时区，默认是 UTC
TIMEZONE='Asia/Shanghai'
#
# CELERY_IMPORTS = ('tasks',)
# # 初始化定时任务
# # CELERY_BEAT_SCHEDULE = {
# #     "sample_task": {
# #         "task": "core.tasks.sample_task",
# #         "schedule": crontab(minute="*/1"),
# #     },
# # }
# celery 序列化与反序列化配置
TASK_SERIALIZER = 'pickle'
RESULT_SERIALIZER = 'pickle'
ACCEPT_CONTENT = ['pickle', 'json']


# celery任务执行结果的超时时间，
TASK_RESULT_EXPIRES = 10
# 设置默认不存结果
IGNORE_RESULT = False

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

# 设置默认的队列名称，如果一个消息不符合其他的队列就会放在默认队列里面，如果什么都不设置的话，
# 数据都会发送到默认的队列中
DEFAULT_QUEUE = "default"

# 设置详细的队列
QUEUES = (
    Queue('task_slow', exchange=Exchange('task_slow'), routing_key='task_slow'),
)
# 配置各个任务分配到不同的任务队列
ROUTES = {
    'celery_task.tasks.xx': {
        'queue': 'task_slow', 'routing_key': 'task_slow'
    }
}

"""
任务指定特定的worker执行
celery做为支持分布式，理论上可以无限扩展worker。默认情况下celery提交任务后，任务会放入名为celery的队列，
所有在线的worker都会从任务队列中获取任务，任一个worker都有可能执行这个任务。
有时候，有时候任务的特殊性或者机器本身的限制，某些任务只能跑在某些worker上。
celery提供了queue在区别不同的worker，很好的支持这种情况。

启动worker时，-Q 指定worker支持的任务列队名, 可以支持多个队列名哦

celery -A celery_tasks worker -l debug -c 4 -Q default,task_slow
任务调用时， queue=*来指定需要执行worker

result = mul.apply_async(args=(2, 2), queue='task_slow')
"""



# celery beat配置（周期性任务设置）
# CELERY_ENABLE_UTC = False
# DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

from .common import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

# 设置白名单
# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1',
# )

# 默认允许所有域名访问
#CORS_ORIGIN_ALLOW_ALL = False


env = 'prod'

REDIS = f"redis://{SECRETS[env]['redis']['host']}:{SECRETS[env]['redis']['port']}"
MONGO = 'mongodb://%s:%s@%s:%s/%s' % (SECRETS[env]['mongo']['user'], SECRETS[env]['mongo']['password'], SECRETS[env]['mongo']['host'], SECRETS[env]['mongo']['port'], SECRETS[env]['mongo']['auth'])


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRETS[env]['db']['name'],
        'HOST': SECRETS[env]['db']['host'],
        'PORT': SECRETS[env]['db']['port'],
        'USER': SECRETS[env]['db']['user'],
        'PASSWORD': SECRETS[env]['db']['password']
    },
}

# Django REST Framework
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_RENDERER_CLASSES': (  # 正式环境下 djangorest测试界面删除
        'rest_framework.renderers.JSONRenderer',
    )
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS}/1", #这里直接使用redis别名作为host ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
    "account": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS}/2",  # 账户相关的缓存放置2号表
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
}
#缓存使用 from django.core.cache import caches  cache=caches['account']

# 日志写入mongo
#LOGGING["handlers"]["mongo"] = {
#     'level': 'INFO',
#     'class': 'util.mongo_handler.MongoHandler',  # 保存到文件，自动切
#     'database': 'mongo_logs',
# }
# LOGGING["loggers"]["mongo"]= {
#             'handlers': ['mongo'],
#             'propagate': True,
#             'level': 'INFO',
#         }
# logger = logging.getLogger('mongo')  logger.info('abc',extra={'name':'hvag'})  为了消除同一个message 可以加点salt logger.info(f'abc-{str(uuid.uuid1())}',extra={'name':'hvag'})



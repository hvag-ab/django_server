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


REDIS_URI = f"redis://:{SECRETS['redis']['password']}@{SECRETS['redis']['host']}:{SECRETS['redis']['port']}"
REDIS_URI = 'mongodb://%s:%s@%s:%s/%s' % (SECRETS['mongo']['user'], SECRETS['mongo']['password'], SECRETS['mongo']['host'], SECRETS['mongo']['port'], SECRETS['mongo']['auth'])


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRETS['db']['name'],
        'HOST': SECRETS['db']['host'],
        'PORT': SECRETS['db']['port'],
        'USER': SECRETS['db']['user'],
        'PASSWORD': SECRETS['db']['password']
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
        "LOCATION": f"{REDIS_URI}/1", #这里直接使用redis别名作为host ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
    "account": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URI}/2",  # 账户相关的缓存放置2号表
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
}
#缓存使用 from django.core.cache import caches  cache=caches['account']

# 日志写入mongo
LOGGING["handlers"]["mongo"] = {
            'class': 'util.mongo_handler.MongoHandler',
            'host': REDIS_URI,  # 通过uri方式配置
            'database_name': 'mongo_logs',
            'collection': 'logs',
            'level': 'INFO',
            'capped': True,
            'capped_max': 100000,
            'capped_size': 100000000
        }

LOGGING["loggers"]["mongo"]= {
            'handlers': ['mongo'],
            'propagate': True,
            'level': 'INFO',
        }
# logger = logging.getLogger('mongo')  logger.info('abc',extra={'name':'hvag'})  为了消除同一个message 可以加点salt logger.info(f'abc-{str(uuid.uuid1())}',extra={'name':'hvag'})



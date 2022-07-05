from .common import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

REDIS_URI = f"redis://{SECRETS['redis']['host']}:{SECRETS['redis']['port']}"
MONGO_URI = 'mongodb://%s:%s' % (SECRETS['mongo']['host'], SECRETS['mongo']['port'])

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


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': ['memcached:11211'],
#         'TIMEOUT': 300,  # 缓存超时时间（默认300秒，None表示永不过期，0表示立即过期）
#         'BINARY': True

#     }
# }

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



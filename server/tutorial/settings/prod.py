from .common import *  # noqa

DEBUG = False


PROD_INSTALLED_APPS = [
    # 'account',
]

INSTALLED_APPS += PROD_INSTALLED_APPS

ALLOWED_HOSTS = [
    '*'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRETS['prod']['db']['name'],
        'HOST': SECRETS['prod']['db']['host'],
        'PORT': SECRETS['prod']['db']['port'],
        'USER': SECRETS['prod']['db']['user'],
        'PASSWORD': SECRETS['prod']['db']['password']
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
        "LOCATION": f"redis://{SECRETS['prod_redis']['host']}:{SECRETS['prod_redis']['port']}/1", #这里直接使用redis别名作为host ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
    "account": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{SECRETS['prod_redis']['host']}:{SECRETS['prod_redis']['port']}/2",  # 账户相关的缓存放置2号表
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
}
#缓存使用 from django.core.cache import caches  cache=caches['account']

#
# LOGGING["handlers"]["mongo"] = {
#     'level': 'INFO',
#     'class': 'util.mongo_handler.SimpleMongoLogHandler',  # 保存到文件，自动切
#     'connection': 'xxx',
#     'max_keep': 1,
#     'collection': 'mongoapp'
# }
# LOGGING["loggers"]["mongo"]= {
#             'handlers': ['mongo'],
#             'propagate': True,
#             'level': 'INFO',
#         }


REDIS = f"redis://{SECRETS['prod']['redis']['host']}:{SECRETS['prod']['redis']['port']}"
from .common import *  # noqa

DEBUG = False


DOCKER_INSTALLED_APPS = [
]

INSTALLED_APPS += DOCKER_INSTALLED_APPS

ALLOWED_HOSTS = [
    '*'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRETS['docker']['db']['name'],
        'HOST': SECRETS['docker']['db']['host'],
        'PORT': SECRETS['docker']['db']['port'],
        'USER': SECRETS['docker']['db']['user'],
        'PASSWORD': SECRETS['docker']['db']['password']
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
        "LOCATION": f"redis://{SECRETS['docker_redis']['host']}:{SECRETS['docker_redis']['port']}/1", #这里直接使用redis别名作为host ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
    "account": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{SECRETS['docker_redis']['host']}:{SECRETS['docker_redis']['port']}/2",  # 账户相关的缓存放置2号表
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",

        }
    },
}




REDIS = f"redis://{SECRETS['docker']['redis']['host']}:{SECRETS['docker']['redis']['port']}"
from .common import *  # noqa

DEBUG = False

env = 'prod'

REDIS = f"redis://{SECRETS[env]['redis']['host']}:{SECRETS[env]['redis']['port']}"
MONGO = 'mongodb://%s:%s@%s:%s/%s' % (SECRETS[env]['mongo']['user'], SECRETS[env]['mongo']['password'], SECRETS[env]['mongo']['host'], SECRETS[env]['mongo']['port'], SECRETS[env]['mongo']['auth'])

PROD_INSTALLED_APPS = [
]

INSTALLED_APPS += PROD_INSTALLED_APPS

ALLOWED_HOSTS = [
    '*'
]


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': SECRETS[env]['db']['name'],
        # 'HOST': SECRETS[env]['db']['host'],
        # 'PORT': SECRETS[env]['db']['port'],
        # 'USER': SECRETS[env]['db']['user'],
        # 'PASSWORD': SECRETS[env]['db']['password']
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR/'app.db'),
    },
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

# 如果要使用channel layer 则必须配置通道层，否则无法获取channel_name
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [f"{REDIS}/3"],
        },
    },
}

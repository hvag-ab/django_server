from django.test.runner import DiscoverRunner

from .common import *  # noqa

env = 'dev'

REDIS = f"redis://{SECRETS[env]['redis']['host']}:{SECRETS[env]['redis']['port']}"
MONGO = 'mongodb://%s:%s@%s:%s/%s' % (SECRETS[env]['mongo']['user'], SECRETS[env]['mongo']['password'], SECRETS[env]['mongo']['host'], SECRETS[env]['mongo']['port'], SECRETS[env]['mongo']['auth'])

DEBUG = True

DEV_INSTALLED_APPS = [
]


INSTALLED_APPS += DEV_INSTALLED_APPS

ALLOWED_HOSTS = [
    '127.0.0.1','localhost'
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
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # 指定缓存使用的引擎
        'LOCATION': 'unique-default',  # 写在内存中的变量的唯一值
        'TIMEOUT': 300,  # 缓存超时时间(默认为300秒,None表示永不过期)
        'OPTIONS': {
            'MAX_ENTRIES': 300,  # 最大缓存记录的数量（默认300）
            'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
        }
    },
    'account': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # 指定缓存使用的引擎
        'LOCATION': 'account',  # 写在内存中的变量的唯一值
        'TIMEOUT': 300,  # 缓存超时时间(默认为300秒,None表示永不过期)
        'OPTIONS': {
            'MAX_ENTRIES': 300,  # 最大缓存记录的数量（默认300）
            'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
        }
    },
}

# 如果要使用channel layer 则必须配置通道层，否则无法获取channel_name
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [f"{REDIS}/3"],
        },
    },
}

# import channels.layers
# channels.layers.get_channel_layer('default')可以自己选择配置的CHANNEL_LAYERS
"""
测试channel layers 是否连接通
>>> import channels.layers
>>> channel_layer = channels.layers.get_channel_layer()
>>> from asgiref.sync import async_to_sync
>>> async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
>>> async_to_sync(channel_layer.receive)('test_channel')
{'type': 'hello'}
"""








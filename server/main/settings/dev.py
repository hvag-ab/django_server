from django.test.runner import DiscoverRunner

from .common import *  # noqa

env = 'dev'

REDIS = f"redis://{SECRETS[env]['redis']['host']}:{SECRETS[env]['redis']['port']}"

DEBUG = True

DEV_INSTALLED_APPS = [
    'app',
    'django_celery_results'
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

# Django REST Framework
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    # 'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',  # 默认的版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],  # 有效的版本
    'VERSION_PARAM': 'version',  # 版本的参数名与URL conf中一致
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 把要发送的邮件显示再控制台上，方便调试
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xxxx@qq.com'  # 帐号
EMAIL_HOST_PASSWORD = 'xxxxxx'  # 授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# 测试的时候不需要创建删除数据库
class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation """

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass


TEST_RUNNER = f'{PROJECT_NAME}.settings.dev.NoDbTestRunner'

try:
    import debug_toolbar  # NOQA
except ImportError:
    pass
else:
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = ['127.0.0.1']  # 这些请求地址显示debug toolbar（注：后面的2个地址是我本地请求地址）
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )

    CONFIG_DEFAULTS = {
        # 因为默认使用google的jquery，国内访问不到
        'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

    DEBUG_TOOLBAR_PATCH_SETTINGS = False




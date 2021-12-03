"""
Django settings for tutorial project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import json
from pathlib import Path
from django.utils.module_loading import import_string


PROJECT_PACKAGE = Path(__file__).resolve().parent.parent
PROJECT_NAME = PROJECT_PACKAGE.parts[-1]

BASE_DIR = PROJECT_PACKAGE.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
config = BASE_DIR / 'config' / 'secrets.json'

# 读取json配置文件
with open(config) as handle:
    SECRETS = json.load(handle)

SECRET_KEY = str(SECRETS['secret_key'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',  # TOKEN 验证
    'django_filters', #pip install django-filter
]

APPS = import_string('config.installed_apps.INSTALLED_APPS')
INSTALLED_APPS += APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = f'{PROJECT_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{PROJECT_NAME}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = False

USE_TZ = True
"""
查出来是utc时间 需要这个方法转化为本地时间
from django.utils.timezone import localtime
result = localtime(some_time_object)
"""
# 时间格式、语言
DATETIME_FORMAT = 'Y-m-d H:i:s'

# ROOT_URLCONF = 'djangoproject.urls.www'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static'
# STATICFILES_DIRS 和STATIC_ROOT 不能同时存在 都是static静态文件查询路径
#STATICFILES_DIRS  = [
#    BASE_DIR / "frontend/dist/static" 比如django控制vue启动 需要这里设置vue静态文件存放文件
#]
# 运行 python3 manage.py collectstatic 就会把django的静态资源打包到STATIC_ROOT 文件里面 后续需要nginx加载静态文件
# nginx 配置django静态资源
"""
location /media  {
    alias /path/to/media;
}
 
location /static {
    alias /path/to/static;
}
如果nginx加载
404 静态资源路径错误 nginx未找到
403 权限错误 chmod 755 /path/to/static #为了保证文件能正确执行，nginx既需要文件的读权限,又需要文件所有父目录的可执行权限。
"""

MEDIA_ROOT = BASE_DIR.parent / 'media'
# 上传图片保存位置
MEDIA_URL = "/media/"  # 浏览器显示图片等 的url 例如 http://localhost:8000/media/.....

# AUTH_USER_MODEL = 'account.UserProfile'  # 因为models使用AbstractUser

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# 跨域设置
# # 设置白名单
# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1',
# )

CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作。

# 默认允许所有域名访问
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

CSRF_COOKIE_NAME = "csrftoken"  # 一定要添加这个 接受前端请求的csrf 否则403 状态 csrf检测拦截
# CSRF_COOKIE_SECURE = True



import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # token的有效期
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # 坑 一定不能把前缀设置为空字符串
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=1)
}


# APPEND_SLASH=True #作用就是自动在网址结尾加'/'

# Logging配置
BASE_LOG_DIR = BASE_DIR.parent / "logs"
# 如果地址不存在，则会自动创建log文件夹
if not BASE_LOG_DIR.is_dir():
    BASE_LOG_DIR.mkdir()
    
LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(levelname)s][%(name)s][%(pathname)s][%(filename)s][%(funcName)s:%(lineno)d]'
                      '[%(message)s]'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'standard',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        # 默认的
        'rotating_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': BASE_LOG_DIR / "django_rotating.log",  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'rotating_time':{
            'level':'INFO',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_LOG_DIR / "django_rotating_time.log",
            'formatter':'standard',
            'when': 'midnight',
            'interval':1,
            'backupCount':5,
            'encoding':'utf-8'
        },
        'json': {
            'level': 'INFO',
            'class': 'util.json_handler.JsonRotatingFileHandler',  # 保存到文件，自动切
            'filename': BASE_LOG_DIR / "django_json.json",
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        "django.request": {
            "handlers": [],
            "level": "DEBUG",
            "propagate": False,
        },
        "debug": {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # 打印sql日志
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
        'rotating_time': {
            'handlers': ['rotating_time'],
            'level': 'DEBUG',
            'propagate': False,  # 向不向更高级别的logger传递
        },
        'rotating_file': {
            'handlers': ['rotating_file'],
            'level': 'INFO'
        },
        'json': {
            'handlers': ['json'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}



REST_FRAMEWORK = {
     'EXCEPTION_HANDLER': 'util.exception.exception_handler',
}




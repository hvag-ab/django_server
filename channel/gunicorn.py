# 并行工作进程数
workers = 4
# 指定每个工作者的线程数
threads = 4
# 监听内网端口5000
bind = '0.0.0.0:9000'
# 设置守护进程,将进程交给supervisor管理
daemon = False
# 工作模式协程
worker_class = 'uvicorn.workers.UvicornWorker'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = 'gunicorn.pid'
# 设置访问日志和错误信息日志路径
# accesslog = '/server/backend/django_server-main/logs/gunicorn_acess.log'
# errorlog = '/server/backend/django_server-main/logs/gunicorn_error.log'
# Whether to send Django output to the error log
capture_output = True
# 设置日志记录水平
loglevel = 'info'

reload=True

#access日志配置，更详细配置请看：https://docs.gunicorn.org/en/stable/settings.html#logging
#`%(a)s`参考示例：'%(a)s "%(b)s" %(c)s' % {'a': 1, 'b' : -2, 'c': 'c'}
#如下配置，将打印ip、请求方式、请求url路径、请求http协议、请求状态、请求的user agent、请求耗时
#示例：[2020-08-19 19:18:19 +0800] [50986]: [INFO] 127.0.0.1 POST /test/v1.0 HTTP/1.1 200 PostmanRuntime/7.26.3 0.088525
access_log_format="%(h)s %(r)s %(s)s %(a)s %(L)s"

#https://github.com/benoitc/gunicorn/issues/2250
logconfig_dict = {
    'version':1,
    'disable_existing_loggers': False,
    #在最新版本必须添加root配置，否则抛出Error: Unable to configure root logger
    "root": {
          "level": "DEBUG",
          "handlers": ["console"] # 对应handlers字典的键（key）
    },
    'loggers':{
        "gunicorn.error": {
            "level": "DEBUG",# 打日志的等级；
            "handlers": ["error_file"], # 对应handlers字典的键（key）；
            #是否将日志打印到控制台（console），若为True（或1），将打印在supervisor日志监控文件logfile上，对于测试非常好用；
            "propagate": 0,
            "qualname": "gunicorn_error"
        },

        "gunicorn.access": {
            "level": "DEBUG",
            "handlers": ["access_file"],
            "propagate": 0,
            "qualname": "access"
        }
    },
    'handlers':{
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*100,# 打日志的大小（此处限制100mb）
            "backupCount": 1,# 备份数量（若需限制日志大小，必须存在值，且为最小正整数）
            "formatter": "generic",# 对应formatters字典的键（key）
            "filename": "../logs/gunicorn_asgi_error.log" #若对配置无特别需求，仅需修改此路径
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*100,
            "backupCount": 1,
            "formatter": "generic",
            "filename": "../logs/gunicorn_asgi_access.log", #若对配置无特别需求，仅需修改此路径
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'generic',
        },

    },
    'formatters':{
        "generic": {
            "format": "%(asctime)s [%(process)d]: [%(levelname)s] %(message)s", # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",# 时间显示格式
            "class": "logging.Formatter"
        }
    }
}

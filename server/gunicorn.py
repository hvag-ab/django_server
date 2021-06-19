
bind = '0.0.0.0:8899' # 监听内网端口
timeout = 90      #超时
woworker_class = 'gevent' #使用gevent模式，还可以使用sync 同步阻塞模式，默认的是sync模式 gthread线程池  gevent：需要下载gevent>=0.13
workers = 9   #进程数 推荐 2*cpu核数 + 1
threads = 8 #指定每个进程开启的线程数 推荐2 - 4*cpu核数 只适用于gthread 方式
reload = True#代码更新时将重启工作，默认为False。此设置用于开发，每当应用程序发生更改时，都会导致工作重新启动。
debug = False
daemon= False #守护进程 #如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题

worker_connections = 2000 #最大客户端并发数量，默认情况下这个值为1000。只适合gevent和eventlet工作模式
max_requests = 2000 #重新启动之前，工作将处理的最大请求数。默认值为0。
graceful_timeout = 30 #接收到restart信号后 可以在给定时间内处理完requests
keepalive = 3 #在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间。
max_requests_jitter = 512  #要添加到max_requests的最大抖动。抖动将导致每个工作的重启被随机化，这是为了避免所有工作被重启。randint(0,max-requests-jitter)
backlog = 2048  #超过最大并发连接所个等待的最大数量，即等待服务的客户的数量。必须是正整数，一般设定在64~2048的范围内，一般设置为2048，超过这个数字将导致客户端在尝试连接时报connection 。 by peer

loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'     #设置gunicorn访问日志格式，错误日志无法设置
# errorlog = 'error.log' #错误日志文件
# accesslog = 'access.log' #访问日志文件
capture_output = True # 获取django控制台的错误
"""
其每个选项的含义如下
        h           remote address
        l           '-'
        u           currently '-', may be user name in future releases
        t           date of the request
        r           status line (e.g. ``GET / HTTP/1.1``)
        s           status
        b           response length or '-'
        f           referer
        a           user agent
        T           request time in seconds
        D           request time in microseconds
        L           request time in decimal seconds
        p           process ID
        {Header}i   request header
        {Header}o   response header
"""

proc_name = 'gunicorn'   #进程名
pidfile = 'gunicorn.pid'
#pythonpath =  如果有必要可以指定python 执行文件目录



#gunicorn -c gunicorn_conf.py main.wsgi:application
#ps -ef | grep gunicorn 查看是否启动
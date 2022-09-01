import asyncio

from django.core.mail import send_mail
from django.conf import settings
import time
from celery.utils.log import get_task_logger
from celery import AsyncResult
from celery_tasks.celery_main import app as celery_app # 导入创建好的celery应用  # 导入创建好的celery应用


@celery_app.task(bind=True) # bind的作用是可以使用self参数
def debug_task(self):
    task_id = self.request.id
    print('Request: {0!r}'.format(self.request)) #dumps its own request information


# 定义任务函数
@celery_app.task(bind=True,ignore_result=True) # ignore_result忽略这个函数的返回结果
def send_email(self,subject,message,from_email,recipient_list,**kwargs):

    try:
        send_mail(subject,message,from_email,recipient_list,**kwargs)
    except Exception as e:
        """
                邮件发送失败，使用retry进行重试

                retry的参数可以有：
                    exc：指定抛出的异常
                    throw：重试时是否通知worker是重试任务
                    eta：指定重试的时间／日期
                    countdown：在多久之后重试（每多少秒重试一次）
                    max_retries：最大重试次数
                """
        self.retry(exc=e, countdown=3, max_retries=5)


@celery_app.task
def mul(x, y):
    time.sleep(10)
    return x * y

# async def async_function(param1, param2):
#     # more async stuff...
#     pass
#
# @celery_app.task(name='tasks.task_name', queue='queue_name')
# def task_name(param1, param2):
#     asyncio.run(async_function(param1, param2))


"""
Django的模型对象不应该作为参数传递 可以传递具体的参数例如id 

from celery.utils.log import get_logger
from celery_tasks.tasks import mul, post_file
from celery import group, chain, chord
logger = get_logger(__name__)
try:
    result = mul.apply_async(args=(2, 2))
    value = result.get() # 等待任务执行完毕后，才会返回任务返回值
    task_id = result.id
    print(result.__dict__) # 结果信息
    print(result.successful()) # 是否成功
    print(result.fail()) # 是否失败
    print(result.ready()) # 是否执行完成
    print(result.state) # 状态 PENDING -> STARTED -> SUCCESS/FAIL
    print(value)
except mul.OperationalError as exc: # 任务异常处理
    logger.exception('Sending task raised: %r', exc)
    
 
 # 通过id 获取状态
res = AsyncResult(task_id)
res.status
# 强制取消任务  注意强制取消后 是否需要捕获任务 如果需要捕获就只能使用 SIGUSR1  这个信号
res.revoke(terminate=True,signal='SIGTERM')
其中，SIGTERM就是默认的Signal，很粗暴；SIGQUIT则比它更粗暴。 至于不在上面的SIGKILL、SIGINT等，也不见得好多少。 如果想要让被终止的任务知道自己被终止，目前只能使用SIGUSR1。
它会在任务正在执行的位置，抛出一个SoftTimeLimitExceeded。 因此，只需要在最外层用try ... except捕获这个异常，就可以进行一些后处理。 但是，由于它的现象和任务超时是类似的，因此需要自行区分。
    
    
组合任务:

多个任务并行执行, group
result = group(mul.s(i, i) for i in range(5))()
result.get()
# [0, 2, 4, 6, 8]

多个任务链式执行，chain：第一个任务的返回值作为第二个的输入参数，以此类推

result = chain(mul.s(1,2), mul.s(3), mul.s(3))()
result.get()
# ((1+2)+3)*3=18
我们将不同的任务签名链接起来创建一个任务链，三个子任务按顺序执行。
def update_page_info(url):
 # fetch_page -> parse_page -> store_page
 chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
 chain()


@app.task()
def fetch_page(url):
 return myhttplib.get(url)


@app.task()
def parse_page(page):
 return myparser.parse_document(page)


@app.task(ignore_result=True)
def store_page_info(info, url):
 PageInfo.objects.create(url=url, info=info)
 
使用on_commit函数处理事务
我们再看另外一个celery中处理事务的例子。这是在数据库中创建一个文章对象的 Django 视图，此时传递主键给任务。
它使用 commit_on_success 装饰器，当视图返回时该事务会被提交，当视图抛出异常时会进行回滚。

 from django.db import transaction
  
 @transaction.commit_on_success
 def create_article(request):
     article = Article.objects.create()
     expand_abbreviations.delay(article.pk)
如果在事务提交之前任务已经开始执行会产生一个竞态条件；数据库对象还不存在。解决方案是使用 on_commit 回调函数来在所有事务提交成功后启动任务。

 from django.db.transaction import on_commit
  
 def create_article(request):
     article = Article.objects.create()
     on_commit(lambda: expand_abbreviations.delay(article.pk))
     
任务延迟执行
my_task.apply_async(countdown=10) # 以秒表示的延迟时间
enable_utc设置为False并且定义了时区时不起作用

预计到达时间
第二种方法是使用eta参数，它需要执行的确切日期和时间。与本机datetime对象，日期为String或Pendulum实例完美配合。
my_task.apply_async(eta=datetime.now(pytz.timezone("Europe/Warsaw"))
my_task.apply_async(eta="2018-02-19 13:41:14+01:00")
my_task.apply_async(eta=pendulum.now("Europe/Warsaw"))

apply_async 参数
 countdown : 设置该任务等待一段时间再执行，单位为s；
# eta : 定义任务的开始时间；eta=time.time()+10;
# expires : 设置任务时间，任务在过期时间后还没有执行则被丢弃；
# retry : 如果任务失败后, 是否重试;使用true或false，默认为true
# shadow：重新指定任务的名字str，覆盖其在日志中使用的任务名称；
# retry_policy : 重试策略.
#   max_retries : 最大重试次数, 默认为 3 次.
#   interval_start : 重试等待的时间间隔秒数, 默认为 0 , 表示直接重试不等待.
#   interval_step : 每次重试让重试间隔增加的秒数, 可以是数字或浮点数, 默认为 0.2
#   interval_max : 重试间隔最大的秒数, 即 通过 interval_step 增大到多少秒之后, 就不在增加了, 可以是数字或者浮点数, 默认为 0.2 .
# routing_key:自定义路由键；
# queue：指定发送到哪个队列；
# exchange：指定发送到哪个交换机；
# priority：任务队列的优先级，0-9之间；
# serializer：任务序列化方法；通常不设置；
# compression：压缩方案，通常有zlib, bzip2
# headers：为任务添加额外的消息；
# link：任务成功执行后的回调方法；是一个signature对象；可以用作关联任务
 
task.apply_async ( ( 2 , 2 ) ,
     compression = 'zlib' ,
     serialize = 'json' ,
     queue = 'priority.high' ,
     routing_key = 'web.add' ,
     priority = 0 ,
     exchange = 'web_exchange' )
"""

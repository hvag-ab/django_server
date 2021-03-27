from django.core.mail import send_mail
from django.conf import settings
import time
from celery.utils.log import get_task_logger
from celery_tasks.celery import app as celery_app # 导入创建好的celery应用  # 导入创建好的celery应用


@celery_app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request)) #dumps its own request information


# 定义任务函数
@celery_app.task(bind=True)
def send_register_active_email(self,to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '欢迎信息'
    message = ''
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为xxx注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)

    print("=========== 执行发送邮件 ===============")

    try:
        send_mail(subject, message, sender, receiver, html_message=html_message)
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
        raise self.retry(exc=e, countdown=3, max_retries=5)


@celery_app.task
def mul(x, y):
    time.sleep(5)
    return x * y


"""
from celery.utils.log import get_logger
from celery_tasks.tasks import mul, post_file
from celery import group, chain, chord
logger = get_logger(__name__)
try:
    result = mul.apply_async(args=(2, 2))
    value = result.get() # 等待任务执行完毕后，才会返回任务返回值
    
    print(result.__dict__) # 结果信息
    print(result.successful()) # 是否成功
    print(result.fail()) # 是否失败
    print(result.ready()) # 是否执行完成
    print(result.state) # 状态 PENDING -> STARTED -> SUCCESS/FAIL
    print(value)
except mul.OperationalError as exc: # 任务异常处理
    logger.exception('Sending task raised: %r', exc)
    
    
组合任务:

多个任务并行执行, group

多个任务链式执行，chain：第一个任务的返回值作为第二个的输入参数，以此类推

result = group(mul.s(i, i) for i in range(5))()
result.get()
# [0, 2, 4, 6, 8]
result = chain(mul.s(1,2), mul.s(3), mul.s(3))()
result.get()
# ((1+2)+3)*3=18
"""

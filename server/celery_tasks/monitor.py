"""
任务状态跟踪和日志
有时候我们需要对任务的执行情况做一些监控，比如失败后报警通知。

celery在装饰器@app.task中提供了base参数，传入重写的Task模块，重新on_*函数就可以控制不同的任务结果

在@app.task提供bind=True，可以通过self获取Task中各种参数

self.request：任务的各种参数


exc:失败时的错误的类型；
task_id:任务的id；
args:任务函数的参数；
kwargs:参数；
einfo:失败时的异常详细信息；
retval:任务成功执行的返回值；


self.update_state: 自定义任务状态, 原有的任务状态：PENDING -> STARTED -> SUCCESS， 如果你想了解STARTED -> SUCCESS之间的一个状态，比如执行的百分比之类，可以通过自定义状态来实现

self.retry: 重试
"""

import celery
import time
from celery.utils.log import get_task_logger
from celery_tasks.celery_main import app as celery_app
from celery.worker.request import Request

logger = get_task_logger(__name__)

class MyRequest(Request):
    'A minimal custom request to log failures and hard time limits.'

    def on_timeout(self, soft, timeout):
        super().on_timeout(soft, timeout)
        if not soft:
            logger.warning(
                'A hard timeout was enforced for task %s',
                self.task.name
            )

    def on_accepted(self, pid, time_accepted):
        super().on_accepted(pid, time_accepted)
        logger.warning(
            f'task {self.task.name}[{self.id}] has start, params_dict={self.request_dict}'
            f'args-{self.args},kwargs-{self.kwargs}'
        )
    ## self.args and self.kwargs 来源于 post_file.apply_async(args=(),kwargs={})

class TaskMonitor(celery.Task):

    Request = MyRequest  # you can use a FQN 'my.package:MyRequest'

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """failed callback"""
        logger.info('task id: {0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        """success callback"""
        logger.info('task id:{} , arg:{} , successful !'.format(task_id, args))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """retry callback"""
        logger.info('task id:{} , arg:{} , retry !  einfo: {}'.format(task_id, args, exc))
    
    @classmethod
    def on_bound(cls,app):
        print("celery 启动的时候执行这个钩子 可用于清除celery意外中断后造成的脏数据")


@celery_app.task(base=TaskMonitor, bind=True, name='post_file')
def post_file(self, file_names, **kwargs): # 这里的**kwargs 来源于 post_file.apply_async(args=(file_name,),kwargs={'id':1}) 
    logger.info(self.request.__dict__)
    print(self.AsyncResult(self.request.id).state)
    try:
        for i, file in enumerate(file_names):
            print('the file %s is posted' % file)
            if not self.request.called_directly:
                self.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': len(file_names)})
            time.sleep(2)
    except Exception as exec:
        raise self.retry(exc=exec, countdown=3, max_retries=5)

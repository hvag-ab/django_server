"""
任务状态跟踪和日志
有时候我们需要对任务的执行情况做一些监控，比如失败后报警通知。

celery在装饰器@app.task中提供了base参数，传入重写的Task模块，重新on_*函数就可以控制不同的任务结果

在@app.task提供bind=True，可以通过self获取Task中各种参数

self.request：任务的各种参数

self.update_state: 自定义任务状态, 原有的任务状态：PENDING -> STARTED -> SUCCESS， 如果你想了解STARTED -> SUCCESS之间的一个状态，比如执行的百分比之类，可以通过自定义状态来实现

self.retry: 重试
"""

import celery
import time
from celery.utils.log import get_task_logger
from celery_tasks.celery import app as celery_app

logger = get_task_logger(__name__)

"""
exc:失败时的错误的类型；
task_id:任务的id；
args:任务函数的参数；
kwargs:参数；
einfo:失败时的异常详细信息；
retval:任务成功执行的返回值；
"""
class TaskMonitor(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """failed callback"""
        logger.info('task id: {0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        """success callback"""
        logger.info('task id:{} , arg:{} , successful !'.format(task_id, args))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """retry callback"""
        logger.info('task id:{} , arg:{} , retry !  einfo: {}'.format(task_id, args, exc))


@celery_app.task(base=TaskMonitor, bind=True, name='post_file')
def post_file(self, file_names):
    logger.info(self.request.__dict__)
    try:
        for i, file in enumerate(file_names):
            print('the file %s is posted' % file)
            if not self.request.called_directly:
                self.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': len(file_names)})
            time.sleep(2)
    except Exception as exec:
        raise self.retry(exc=exec, countdown=3, max_retries=5)
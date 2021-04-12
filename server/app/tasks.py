import time
from celery_tasks.celery import app as celery_app



@celery_app.task
def add(x, y):
    time.sleep(5)
    return x + y
import time
from celery_tasks.celery_main import app as celery_app

@celery_app.task
def add(x, y):
    time.sleep(3)
    return x + y

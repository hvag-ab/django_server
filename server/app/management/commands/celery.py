import sys

import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload


class Command(BaseCommand):
    def handle(self, *args, **options):
        autoreload.run_with_reloader(self._restart_celery)

    @classmethod
    def _restart_celery(cls):
        if sys.platform == "win32":
            cls.run('taskkill /f /t /im celery.exe')
            cls.run('celery -A celery_tasks.celery_main worker --loglevel=info --pool=solo')
        else:  # probably ok for linux2, cygwin and darwin. Not sure about os2, os2emx, riscos and atheos
            cls.run('pkill celery')
            cls.run('celery -A celery_tasks.celery_main worker -l info')

    @staticmethod
    def run(cmd):
        subprocess.call(shlex.split(cmd))
        
"""
 仅适用于测试环境
 测试环境中 打开shell 然后 进入到manage.py 同级目录 
 输入 python manage.py celery  就启动了celery了 然后app下面的文件存在变动 就会自动重新celery
 
"""

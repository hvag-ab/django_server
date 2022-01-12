# 通过脚本调用django中的函数 变量

import os, sys, django
from pathlib import Path

DJANGO_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(DJANGO_DIR))# 否则会报错ModuleNotFoundError
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.dev")
django.setup()

from app.models import Colors

f = Colors.objects.all()
print(f)

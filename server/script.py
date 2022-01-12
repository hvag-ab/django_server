# 通过脚本调用django中的函数 变量

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.dev")
django.setup()

from app.models import Colors

f = Colors.objects.all()
print(f)

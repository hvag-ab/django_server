"""
说明
manage.py 启动测试环境 已经配置好dev的setting
gunicorn 启动 wsgi.py 已经配置好prod的setting
如果使用 supervisorctl 启动 那么要在ini里面配置好环境变量 方便使用哪一个setting启动
例如 添加 environment=DJANGO_SETTINGS_MODULE=adminset.settings.dev
docker 启动 默认用gunicorn启动 那么就默认prod启动 当然也可以通过docker添加环境变量启动

修改tutorial名称 需要修改
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings.dev")
分别在manage.py ,wsgi.py, celery_config, celery_main
"""







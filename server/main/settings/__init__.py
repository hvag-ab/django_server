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

当dev和prod的数据不一样的时候  迁移数据库prod表 要用
 python3 manage.py migrate --settings=main.settings.prod
 
 当迁移的模型中 如果有一些表已经在数据库中存在 迁移办法
 0. 删除所有app下的 migrations文件夹的文件 __init__.py不能删除
 1. 先把已经存在的表 模型在django中注释掉
 2. 然后python3 manage.py makemigrations  python3 manage.py migrate
 3. 然后把注释掉的模型取消注释、
 4. 然后python3 manage.py makemigrations  python3 manage.py migrate --fake
 5. 如果这张表含有其他外键关联 那么  就取消掉注释恢复那些关联这张表外键的模型
 6. 然后python3 manage.py makemigrations  python3 manage.py migrate
""" 







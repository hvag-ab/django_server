import traceback

from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.contrib import admin

# from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name='index.html')) # 有时候不需要启动前端 直接启动django就运行前端打包好的代码 需要这个
]

app_urls = getattr(settings,'APPS', [])

for app_name in app_urls:
    try:
        urlpatterns.append(path(f'api/<str:version>/{app_name}/',include('{}.urls'.format(app_name))))
    except Exception as e:
        print(traceback.format_exc())



if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import serve

    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]


    urlpatterns += [
        # 测试环境下 django 显示 静态问价 例如 图片 文件  js css文件
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

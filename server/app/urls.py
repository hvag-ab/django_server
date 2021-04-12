from django.urls import path
from . import views

app_name= 'app' #方便reverse url获取  reverse(app:non) = path('non/'....

urlpatterns = [
    path('non/', views.NonSerialize.as_view(),name='non'),
    path('api/', views.API.as_view(),name='api'),
    path('create/',views.CreateAPI.as_view(),name='create'),
    path('detail/<int:pk>/', views.DetailAPI.as_view(),name="detail"),
    path('list/', views.ListView.as_view(),name="list"),
    path('retrive/', views.Retrive.as_view(),name="retrive"),
    # 文件
    path('upload_file/', views.UploadFileView.as_view(),name="upload"),
    path('upload_excel/', views.UploadExcel.as_view(),name="upload_excel"),
    path('download_excel/', views.Download.as_view(),name="download_excel"),
    # 缓存
    path('page_cache/',views.PageCacheView.as_view(),name='page_cache'),
    path('http_cache/',views.HttpCacheView.as_view(),name='http_cache'),
    # celery
    path('celery_add/',views.CeleryAdd.as_view(),name='celery_add'),
    path('celery_mul/',views.CeleryMul.as_view(),name='celery_mul'),
]

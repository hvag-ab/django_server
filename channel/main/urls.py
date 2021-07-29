"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from consumers.user_correspondence import UserConsumer
from consumers.group_correspondence import GroupConsumer
from consumers.views import test,LuckyLoadUrl

urlpatterns = [
    # 必须需要这个 否则会报错
    path('test/',test),
    path('admin/', admin.site.urls),
]


websocket_urlpatterns = [
    # 前端请求websocket连接
    path('wx/', UserConsumer.as_asgi()),
    path('ws/<str:group_name>/', GroupConsumer.as_asgi()),
]

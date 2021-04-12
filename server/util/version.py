from rest_framework.versioning import URLPathVersioning,QueryParameterVersioning


# 视图 versioning_class = URLPathVersioning
class APIVersioning(URLPathVersioning):
    default_version = 'v2' # 默认版本
    allowed_versions = ['v1','v2']  # 允许的版本
    version_param = 'version' # URL中获取值的key


"""
urlpatterns = [
    url('api/<str:version>/test/', TestView.as_view(), name='test'),
]

class TestView(APIView):
    versioning_class = APIVersioning
"""
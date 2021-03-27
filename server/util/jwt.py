
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
# from django.db.models import Q

# 视图中加入这两个认证
# permission_classes = (IsAuthenticated,)  # 必须是注册的用户才能访问 注意
# authentication_classes = (JSONWebTokenAuthentication,)

from rest_framework_jwt.settings import api_settings

def get_token(user):

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

# # DRF配置
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     )
# }
#
# # JWT SET
# import datetime
#
# JWT_AUTH = {
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_AUTH_HEADER_PREFIX': 'JWT',
#     'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',  # 默认只返回token 如果需要新增其他key 需要自定义如上
# }
#
# # 设置邮箱和用户名和手机号均可登录
# AUTHENTICATION_BACKENDS = (
#     'users.views.CustomBackend',
#
# )
#
#
# class CustomBackend(ModelBackend):
#     """
#     自定义用户验证规则
#     """
#
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#             # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
#             # 后期可以添加邮箱验证
#             user = User.objects.get(
#                 Q(username=username) | Q(mobile=username))
#             # django的后台中密码加密：所以不能password==password
#             # UserProfile继承的AbstractUser中有def check_password(self,
#             # raw_password):
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None


# url
"""
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns += [
    path(r'api-token-auth/', obtain_jwt_token)
]

#如果你使用用户名admin和密码admin123456创建了用户，则可以通过在终端中执行以下操作来测试JWT是否正常工作。
"$ curl -X POST -d "username=admin&password=admin123456" http://127.0.0.1:8000/api-token-auth/"

现在访问需要认证的API时，就必须要包含Authorization: JWT <your_token> 头信息了：

$ curl -H "Authorization: JWT <your_token>" http://127.0.0.1:8000/virtual/



刷新Token
如果JWT_ALLOW_REFRESH为True，可以“刷新”未过期的令牌以获得具有更新到期时间的全新令牌。像如下这样添加一个URL模式：

from rest_framework_jwt.views import refresh_jwt_token
urlpatterns += [
    url(r'^api-token-refresh/', refresh_jwt_token)
]
使用方式就是将现有令牌传递到刷新API，如下所示: {"token": EXISTING_TOKEN}。请注意，只有非过期 的令牌才有效。另外，响应JSON看起来与正常获取令牌端点{"token": NEW_TOKEN}相同。

$ curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://localhost:8000/api-token-refresh/
可以重复使用令牌刷新（token1 -> token2 -> token3），但此令牌链存储原始令牌（使用用户名/密码凭据获取）的时间。作为orig_iat，你只能将刷新令牌保留至JWT_REFRESH_EXPIRATION_DELTA。

刷新token以获得新的token的作用在于，持续保持活跃用户登录状态。比如通过用户密码获得的token有效时间为1小时，那么也就意味着1小时后此token失效，用户必须得重新登录，这对于活跃用户来说其实是多余的。如果这个用户在这1小时内都在浏览网站，我们不应该让用户重新登录，就是在token没有失效之前调用刷新接口为用户获得新的token。

认证Token
在一些微服务架构中，身份验证由单个服务处理。此服务负责其他服务委派确认用户已登录此身份验证服务的责任。这通常意味着其他服务将从用户接收JWT传递给身份验证服务，并在将受保护资源返回给用户之前等待JWT有效的确认。添加以下URL模式：

from rest_framework_jwt.views import verify_jwt_token
urlpatterns += [
    url(r'^api-token-verify/', verify_jwt_token)
]
将Token传递给验证API，如果令牌有效，则返回令牌，返回状态码为200。否则，它将返回400 Bad Request以及识别令牌无效的错误。

手动创建Token
有时候你可能希望手动生成令牌，例如在创建帐户后立即将令牌返回给用户。或者，你需要返回的信息不止是Token，可能还有用户权限相关值。你可以这样做：

复制代码
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

payload = jwt_payload_handler(user)
token = jwt_encode_handler(payload)
复制代码
其他设置
你可以覆盖一些其他设置，比如变更Token过期时间，以下是所有可用设置的默认值。在settings.py文件中设置。

复制代码
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    // 这是用于签署JWT的密钥，确保这是安全的，不共享不公开的
    'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    // 如果秘钥是错误的，它会引发一个jwt.DecodeError
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    // Token过期时间设置
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    // 是否开启允许Token刷新服务，及限制Token刷新间隔时间，从原始Token获取开始计算
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    // 定义与令牌一起发送的Authorization标头值前缀
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

"""

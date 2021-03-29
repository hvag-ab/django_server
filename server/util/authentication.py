from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings


# restful视图中加入这两个认证
# permission_classes = (IsAuthenticated,)  # 必须是注册的用户才能访问 注意
# authentication_classes = (JSONWebTokenAuthentication,)

# 自定义 token 认证  获取user信息 认证失败返回401状态码
class Authentication(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        # token = self.get_authorization_header(request)
        # do something
        # 第一个参数必须返回 user实例 供 request.user 调用
        # return (user, token)
        return super().authenticate(request)

    def get_authorization_header(self, request):
        """
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        # auth = 'Token 401f7ac837da42b97f613d789819ff93537bee6a'
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode('iso-8859-1')

        auth = auth.split()
        if len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        keyword = auth[0].decode()
        token = auth[1].decode()

        if keyword != self.keyword:
            raise exceptions.AuthenticationFailed(f'缺少关键字{self.keyword}开头')

        return token


# jwt 认证
def user2token(user):

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

# # JWT SET
# import datetime
#
# JWT_AUTH = {
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
#      #是否开启允许Token刷新服务，及限制Token刷新间隔时间，从原始Token获取开始计算
#     'JWT_ALLOW_REFRESH': False,
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_AUTH_HEADER_PREFIX': 'JWT',
# }

"""
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
"""
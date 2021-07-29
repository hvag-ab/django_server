from channels.auth import AuthMiddlewareStack
# 继承settings中的allow host
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from .urls import websocket_urlpatterns
from util.authentication import WebSocketAuthMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        WebSocketAuthMiddleware(  # 认证中间件
            URLRouter(
                # 这里配置websocket的路由
                websocket_urlpatterns
            )
        ),
    )
})

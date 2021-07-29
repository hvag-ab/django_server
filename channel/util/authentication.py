from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.auth import AuthMiddleware, UserLazyObject
from django import http


@database_sync_to_async
def get_user(scope):
    protocol = dict(scope['headers']).get(b'sec-websocket-protocol', b'').decode()

    query_params = http.QueryDict(scope.get("query_string", ""))

    # print(query_params)
    # print(dict(scope['headers']))

    user = None

    return user or AnonymousUser()


class WebSocketAuthMiddleware(AuthMiddleware):

    def populate_scope(self, scope):
        # Make sure we have a session
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user(scope)

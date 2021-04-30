import traceback
from django.core.exceptions import PermissionDenied
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (AuthenticationFailed, MethodNotAllowed, NotAuthenticated,
                                       PermissionDenied as RestPermissionDenied,
                                       ValidationError,NotFound)
from django.http import Http404


def exception_handler(exc, content):

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        status = 401
        msg = exc.detail if hasattr(exc, 'detail') else '用户未登录或登录态失效，请使用登录链接重新登录'

    elif isinstance(exc, PermissionDenied) or isinstance(exc, RestPermissionDenied):
        status = 403
        msg = exc.detail if hasattr(exc, 'detail') else '该用户没有该权限功能'

    elif isinstance(exc, ValidationError):
        status = 407
        msg = exc.detail

    elif isinstance(exc, MethodNotAllowed):
        status = 405
        msg = exc.detail

    elif isinstance(exc, Http404):
        # 更改返回的状态为为自定义错误类型的状态码
        status = 404
        msg = "Not found"

    elif isinstance(exc,NotFound):
        status = 404
        msg = exc.detail

    else:
        # 调试模式
        print(traceback.format_exc())
        if settings.DEBUG:
            raise exc
        status = 500
        msg = traceback.format_exc(limit=2)
        data = content['request'].data or content['request'].query_params
        msg += '\n->传入的参数：' + str(data)


    return Response(status=status,data=dict(code=False,msg=msg))


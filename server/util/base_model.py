from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .paginations import CustomPagination
from .response import JsResponse


class BasePostView(CreateAPIView):

    serializer_class = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return JsResponse(data=response.data)

    def perform_create(self, serializer):
        # 新增直接保存 如果不是新增比如更新或者其他逻辑
        serializer.save()

        # 其他逻辑 获取参数验证后的data
        # data = serializer.data
        # do something


class BaseListView(ListAPIView):
    queryset = None
    serializer_class = None
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        request = self.request
        params = request.query_params
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return JsResponse(data=response.data)


class BaseView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]





